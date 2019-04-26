from enum import Enum
from typing import List

import requests
from requests import Response

from model import TimeOffRequest, ChangeTimeOffRequestStatus
from bamboohr_schema import TimeOffRequestSchema, ChangeTimeOffRequestStatusSchema


class Request(Enum):
    get = 'get'
    put = 'put'


class HrApi(object):
    def get_time_off_requests(self) -> List[TimeOffRequest]:
        raise NotImplementedError('implemented in subclass')

    def approve_request(self, request_id: str, note: str) -> bool:
        raise NotImplementedError('implemented in subclass')


class BambooHr(HrApi):

    def __init__(self, company_id: str, api_key: str):
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.api_key = api_key
        self.base_url = 'https://api.bamboohr.com/api/gateway.php/{0}/v1/'.format(company_id)

    def _request(self, request: Request, path: str, **kwargs) -> Response:
        return requests.request(
            method=request.value,
            url=self.base_url + path,
            headers=self.headers,
            auth=(self.api_key, ''),
            **kwargs
        )

    def get_time_off_requests(self) -> List[TimeOffRequest]:
        resp = self._request(Request.get, "time_off/requests?status=requested")
        resp.raise_for_status()

        return TimeOffRequestSchema().load(resp.json(), many=True).data

    def approve_request(self, request_id: str, note: str) -> bool:
        change_request = ChangeTimeOffRequestStatus('approved', note)
        data = ChangeTimeOffRequestStatusSchema().dump(change_request).data

        resp = self._request(Request.put, 'time_off/requests/{0}/status/'.format(request_id), data=json.dumps(data))

        return resp.status_code == 200
