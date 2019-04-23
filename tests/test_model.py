import json
import os
import unittest
from typing import List

from bamboohr_schema import TimeOffRequestSchema
from model import TimeOffRequest, Amount, TimeOffRequestStatus, AmountUnit

FILENAME_TIME_OFF_REQUESTS = os.path.join(os.path.dirname(__file__), 'stubs/time_off_requests.json')


class TestModel(unittest.TestCase):

    def setUp(self):
        f = open(FILENAME_TIME_OFF_REQUESTS)
        f_content = f.read()
        self.time_off_requests_json = json.loads(f_content)
        f.close()

    def test_parse_requests(self):
        requests: List[TimeOffRequest] = TimeOffRequestSchema().load(self.time_off_requests_json, many=True).data
        self.assertEqual(len(requests), 5)

        self.assertEqual(requests[0].id, '15325')
        self.assertEqual(requests[0].amount.unit, AmountUnit.days)
        self.assertEqual(requests[0].status, TimeOffRequestStatus.canceled)

        self.assertEqual(requests[1].id, '35612')
        self.assertEqual(requests[2].id, '11809')
        self.assertEqual(requests[3].id, '29859')
        self.assertEqual(requests[4].id, '35595')

    def test_is_too_many_days(self):
        long_request = TimeOffRequest('1', '1', "John", TimeOffRequestStatus.requested, Amount(AmountUnit.days, 6))
        self.assertEqual(long_request.is_auto_approvable(), False)

    def test_is_requested_state(self):
        for s in TimeOffRequestStatus:
            req = TimeOffRequest('1', '1', "John", s, Amount(AmountUnit.days, 3))
            self.assertEqual(req.is_auto_approvable(), s == TimeOffRequestStatus.requested)


if __name__ == '__main__':
    unittest.main()
