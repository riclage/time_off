import enum
from enum import Enum
from typing import List, Tuple

import wikiquote

from bamboohr_api import HrApi


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
