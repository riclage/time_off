from marshmallow import Schema, fields, post_load


class ChangeTimeOffRequestStatusSchema(Schema):
    status = fields.Str()
    note = fields.Str()


class AmountSchema(Schema):
    unit = fields.Str()
    amount = fields.Float()

    @post_load
    def make_request_status(self, data):
        return Amount(**data)


class TimeOffRequestStatusSchema(Schema):
    status = fields.Str()
    lastChanged = fields.Date(attribute="last_changed")

    @post_load
    def make_request_status(self, data):
        return TimeOffRequestStatus(**data)


class TimeOffRequestSchema(Schema):
    id = fields.Str(attribute="request_id")
    employeeId = fields.Str(attribute="employee_id")
    status = fields.Nested(TimeOffRequestStatusSchema())
    amount = fields.Nested(AmountSchema())

    @post_load
    def make_request(self, data):
        return TimeOffRequest(**data)


class ChangeTimeOffRequestStatus(object):
    def __init__(self, status, note):
        self.status = status
        self.note = note


class Amount(object):
    def __init__(self, unit, amount):
        self.unit = unit
        self.amount = amount


class TimeOffRequestStatus(object):
    def __init__(self, status, last_changed):
        self.status = status
        self.last_changed = last_changed


class TimeOffRequest(object):
    def __init__(self, request_id, employee_id, status, amount):
        self.id = request_id
        self.employee_id = employee_id
        self.status = status
        self.amount = amount

    def is_auto_approvable(self) -> bool:
        return True if self.amount.unit == 'days' and self.amount.amount <= 5 else False
