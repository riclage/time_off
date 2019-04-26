import unittest

from mocks import MockQuoteApi, MockHrApi
from model import TimeOffRequest, TimeOffRequestStatus, Amount, AmountUnit
from use_cases import GetQuoteOfTheDayUseCase, AutoApproveRequestsUseCase, AutoApproveResult


class TestModel(unittest.TestCase):

    def setUp(self):
        api = MockQuoteApi("text", "author")
        self.quote_use_case = GetQuoteOfTheDayUseCase(api)

    def testQuoteOfTheDay(self):
        self.assertEqual(self.quote_use_case.get_quote_of_the_day(), "\"text\" [author]")

    def testEmptyAutoApproveRequest(self):
        api = MockHrApi([], [])
        use_case = AutoApproveRequestsUseCase(api, self.quote_use_case)

        self.assertEqual(use_case.auto_approve_requests(), [])

    def testAutoApproveRequestList(self):
        request1 = TimeOffRequest("1", "1", "", TimeOffRequestStatus.requested, Amount(AmountUnit.days, 1))
        request2 = TimeOffRequest("2", "1", "", TimeOffRequestStatus.requested, Amount(AmountUnit.days, 1))
        request3 = TimeOffRequest("3", "1", "", TimeOffRequestStatus.requested, Amount(AmountUnit.days, 100))
        api = MockHrApi([request1, request2, request3], [True, False, True])

        use_case = AutoApproveRequestsUseCase(api, self.quote_use_case)
        result = use_case.auto_approve_requests()

        self.assertEqual(result[0][0], AutoApproveResult.success)
        self.assertEqual(result[1][0], AutoApproveResult.fail)
        self.assertEqual(result[2][0], AutoApproveResult.not_auto_approvable)
