import wikiquote

from bamboohr_api import HrApi


class GetQuoteOfTheDayUseCase(object):

    @staticmethod
    def get_quote_of_the_day() -> str:
        quote = wikiquote.quote_of_the_day()
        return "\"{0}\" [{1}]".format(quote[0], quote[1])


class AutoApproveRequestsUseCase(object):

    def __init__(self, hr_api: HrApi, quotes_use_case: GetQuoteOfTheDayUseCase):
        self.hr_api = hr_api
        self.quotes_use_case = quotes_use_case

    def auto_approve_requests(self) -> [str]:
        note = self.quotes_use_case.get_quote_of_the_day()
        request_list = self.hr_api.get_time_off_requests()

        status_msgs = []
        for request in request_list:
            if request.is_auto_approvable():
                if self.hr_api.approve_request(request.id, note):
                    status_msgs.append("Approved request id {0} from {1}".format(request.id, request.employee_name))
                else:
                    status_msgs.append(
                        "Failed to approve request id {0} from {1}".format(request.id, request.employee_name))
            else:
                status_msgs.append(
                    "Request id {0} from {1} is not auto-approvable".format(request.id, request.employee_name))

        return status_msgs
