import enum
from enum import Enum
from typing import List, Tuple

import requests
import wikiquote

from bamboohr_api import HrApi


class EmailApi(object):
    def send_email(self, from_address: str, to_address: str, to_name: str, title: str, body: str) -> bool:
        raise NotImplementedError('implemented in subclass')


class MailGunEmailApi(EmailApi):

    def __init__(self, post_url: str, api_key: str):
        self.post_url = post_url
        self.api_key = api_key

    def send_email(self, from_address: str, to_address: str, to_name: str, title: str, body: str) -> bool:
        result = requests.post(
            "{0}/messages".format(self.post_url),
            auth=("api", self.api_key),
            data={"from": from_address,
                  "to": [to_address, to_name],
                  "subject": title,
                  "text": body})

        return result.status_code == 200


class QuoteApi(object):
    def get_quote_of_the_day(self) -> Tuple[str, str]:
        raise NotImplementedError('implemented in subclass')


class WikiQuoteApi(QuoteApi):

    def get_quote_of_the_day(self) -> Tuple[str, str]:
        return wikiquote.quote_of_the_day()


class GetQuoteOfTheDayUseCase(object):

    def __init__(self, quote_api: QuoteApi):
        self.quote_api = quote_api

    def get_quote_of_the_day(self) -> str:
        quote = self.quote_api.get_quote_of_the_day()
        return "\"{0}\" [{1}]".format(quote[0], quote[1])


class AutoApproveResult(Enum):
    success = enum.auto()
    fail = enum.auto()
    not_auto_approvable = enum.auto()


class AutoApproveRequestsUseCase(object):

    def __init__(self, hr_api: HrApi, quotes_use_case: GetQuoteOfTheDayUseCase):
        self.hr_api = hr_api
        self.quotes_use_case = quotes_use_case

    def auto_approve_requests(self) -> List[Tuple[AutoApproveResult, str]]:
        note = self.quotes_use_case.get_quote_of_the_day()
        request_list = self.hr_api.get_time_off_requests()

        status_msgs: List[Tuple[AutoApproveResult, str]] = []
        for request in request_list:
            if request.is_auto_approvable():
                if self.hr_api.approve_request(request.id, note):
                    status_msgs.append(
                        (AutoApproveResult.success,
                         "Approved request id {0} from {1}".format(request.id, request.employee_name)))
                else:
                    status_msgs.append(
                        (AutoApproveResult.fail,
                         "Failed to approve request id {0} from {1}".format(request.id,
                                                                            request.employee_name)))
            else:
                status_msgs.append(
                    (AutoApproveResult.not_auto_approvable,
                     "Request id {0} from {1} is not auto-approvable".format(request.id,
                                                                             request.employee_name)))

        return status_msgs


class ReportAutoApproveResultUseCase(object):

    def __init__(self, email_api: EmailApi):
        self.email_api = email_api

    def report_results(self, results: List[Tuple[AutoApproveResult, str]], report_to_email: str, report_to_name: str):
        if len(results) == 0:
            print("Nothing to approve")
        else:
            msgs = ["[{0}] {1}".format(status.name, msg) for status, msg in results]
            msg_to_send = "\n".join(msgs)
            print(msg_to_send)

            send_email_result = self.email_api.send_email(
                "no-reply@nobody.com",
                report_to_email,
                report_to_name,
                "Time Off Auto Approve Results",
                msg_to_send
            )

            if not send_email_result:
                print("Failed to report results by email")
