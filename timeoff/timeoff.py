import json
from typing import List

import requests

from model import TimeOffRequest, ChangeTimeOffRequestStatus
from bamboohr_schema import TimeOffRequestSchema, ChangeTimeOffRequestStatusSchema

import wikiquote

HOST = "https://{0}:x@api.bamboohr.com"
GET_REQUESTS_URL = "/api/gateway.php/{0}/v1/time_off/requests?status=requested"
CHANGE_REQUEST_STATUS_URL = "/api/gateway.php/{0}/v1/time_off/requests/{1}/status/"


def get_time_off_requests() -> List[TimeOffRequest]:
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    resp = requests.get(HOST + GET_REQUESTS_URL, headers=headers)

    if resp.status_code == 200:
        return TimeOffRequestSchema().load(resp.json(), many=True).data
    else:
        raise requests.ConnectionError("Expected status code 200, but got {}".format(resp.status_code))


def approve_request(request_id: str) -> bool:
    quote = wikiquote.quote_of_the_day()
    note = "\"{0}\" [{1}]".format(quote[0], quote[1])

    change_request = ChangeTimeOffRequestStatus('approved', note)
    data = ChangeTimeOffRequestStatusSchema().dump(change_request).data

    url = HOST + CHANGE_REQUEST_STATUS_URL
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    resp = requests.put(url.format(request_id), data=json.dumps(data), headers=headers)

    return resp.status_code == 200


request_list = get_time_off_requests()

for request in request_list:
    if request.is_auto_approvable():
        if approve_request(request.id):
            print("Approved request id {0}".format(request.id))
