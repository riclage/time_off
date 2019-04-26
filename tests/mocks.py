from typing import List, Tuple

from bamboohr_api import HrApi
from model import TimeOffRequest
from use_cases import QuoteApi


class MockQuoteApi(QuoteApi):

    def __init__(self, quote_text: str, author: str):
        self.quote = (quote_text, author)

    def get_quote_of_the_day(self) -> Tuple[str, str]:
        return self.quote


class MockHrApi(HrApi):

    def __init__(self, requests: List[TimeOffRequest], approvable: List[bool]):
        self.requests = requests
        self.approvable = approvable

    def get_time_off_requests(self) -> List[TimeOffRequest]:
        return self.requests

    def approve_request(self, request_id: str, note: str) -> bool:
        for request, approvable in zip(self.requests, self.approvable):
            if request.id == request_id:
                return approvable

        return False
