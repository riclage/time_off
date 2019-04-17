from enum import Enum


class AmountUnit(Enum):
    days = 'days'


class ChangeTimeOffRequestStatus(object):
    def __init__(self, status, note):
        self.status = status
        self.note = note


class Amount(object):
    def __init__(self, unit: AmountUnit, amount: float):
        self.unit = unit
        self.amount = amount


class TimeOffRequestStatus(Enum):
    approved = 'approved'
    denied = 'denied'
    canceled = 'canceled'
    superceded = 'superceded'
    requested = 'requested'


class TimeOffRequest(object):
    def __init__(self, request_id: str, employee_id: str, name: str, status: TimeOffRequestStatus,
                 amount: Amount):
        self.id = request_id
        self.employee_id = employee_id
        self.employee_name = name
        self.status = status
        self.amount = amount

    def is_auto_approvable(self) -> bool:
        return True if self.status == TimeOffRequestStatus.requested \
                       and self.amount.unit == AmountUnit.days \
                       and self.amount.amount <= 3 \
            else False
