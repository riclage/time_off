import json
from typing import List

import requests

from model import TimeOffRequest, ChangeTimeOffRequestStatus
from bamboohr_schema import TimeOffRequestSchema, ChangeTimeOffRequestStatusSchema

import wikiquote

HOST = "https://{0}:x@api.bamboohr.com"
GET_REQUESTS_URL = "/api/gateway.php/{0}/v1/time_off/requests?status=requested"
CHANGE_REQUEST_STATUS_URL = "/api/gateway.php/{0}/v1/time_off/requests/{1}/status/"


class BambooHR(object):

    def __init__(self, company_key: str, api_key: str):
        self.headers = {'Accept': 'application/json'}
        self.api_key = api_key
        self.base_url = 'https://api.bamboohr.com/api/gateway.php/{0}/{1}/'.format(self.subdomain, self.api_version)"

    def get_time_off_requests(self) -> List[TimeOffRequest]:
        resp = requests.get(HOST + GET_REQUESTS_URL, headers=self.headers)
        resp.raise_for_status()

        return TimeOffRequestSchema().load(resp.json(), many=True).data

    def approve_request(self, request_id: str) -> bool:
        quote = wikiquote.quote_of_the_day()
        note = "\"{0}\" [{1}]".format(quote[0], quote[1])

        change_request = ChangeTimeOffRequestStatus('approved', note)
        data = ChangeTimeOffRequestStatusSchema().dump(change_request).data

        url = HOST + CHANGE_REQUEST_STATUS_URL
        resp = requests.put(url.format(request_id), data=json.dumps(data), headers=self.headers)

        return resp.status_code == 200
