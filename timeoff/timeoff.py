from bamboohr_api import BambooHR

bamboohr = BambooHR('your company id', 'your api key')

request_list = bamboohr.get_time_off_requests()

status_msgs = []
for request in request_list:
    if request.is_auto_approvable():
        if bamboohr.approve_request(request.id):
            status_msgs.append("Approved request id {0} from {1}".format(request.id, request.employee_name))
        else:
            status_msgs.append("Failed to approve request id {0} from {1}".format(request.id, request.employee_name))
    else:
        status_msgs.append("Request id {0} from {1} is not auto-approvable".format(request.id, request.employee_name))

for msg in status_msgs:
    print(msg)
