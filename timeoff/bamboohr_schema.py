from marshmallow import Schema, fields, post_load
from marshmallow.validate import OneOf

from model import Amount, TimeOffRequestStatus, TimeOffRequest, AmountUnit


class ChangeTimeOffRequestStatusSchema(Schema):
    status = fields.Str()
    note = fields.Str()


class AmountSchema(Schema):
    unit = fields.Str()
    amount = fields.Float()

    @post_load
    def make_request_status(self, data):
        return Amount(AmountUnit[data['unit']], data['amount'])


class TimeOffRequestStatusSchema(Schema):
    status = fields.Str(validate=OneOf([s.value for s in TimeOffRequestStatus]))

    @post_load
    def make_request_status(self, data):
        return TimeOffRequestStatus[data['status']]


class TimeOffRequestSchema(Schema):
    id = fields.Str(attribute="request_id")
    employeeId = fields.Str(attribute="employee_id")
    status = fields.Nested(TimeOffRequestStatusSchema())
    amount = fields.Nested(AmountSchema())

    @post_load
    def make_request(self, data):
        return TimeOffRequest(**data)
