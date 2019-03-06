from bamboohr_api import BambooHR

bamboohr = BambooHR()

request_list = bamboohr.get_time_off_requests()

for request in request_list:
    if request.is_auto_approvable():
        if bamboohr.approve_request(request.id):
            print("Approved request id {0}".format(request.id))
