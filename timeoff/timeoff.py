from bamboohr_api import get_time_off_requests, approve_request

request_list = get_time_off_requests()

for request in request_list:
    if request.is_auto_approvable():
        if approve_request(request.id):
            print("Approved request id {0}".format(request.id))
