from datetime import date
from typing import Optional

LEAVE_TYPES = {
    "annual": 18,
    "sick": 10,
    "maternity": 182,
    "paternity": 5,
}

leave_records: dict = {}
leave_balances: dict = {}
_next_leave_id: int = 1


def _init_balance(emp_id: int) -> None:
    if emp_id not in leave_balances:
        leave_balances[emp_id] = {lt: days for lt, days in LEAVE_TYPES.items()}


def apply_leave(emp_id: int, leave_type: str, days: int, reason: str) -> dict:
    global _next_leave_id
    if leave_type not in LEAVE_TYPES:
        raise ValueError(f"Invalid leave type: {leave_type}")
    if days <= 0:
        raise ValueError("Days must be positive")
    if not check_leave_eligibility(emp_id, leave_type):
        raise ValueError(f"Insufficient {leave_type} leave balance")

    record = {
        "leave_id": _next_leave_id,
        "emp_id": emp_id,
        "leave_type": leave_type,
        "days": days,
        "reason": reason,
        "status": "pending",
        "applied_on": date.today().isoformat(),
        "approved_by": None,
        "rejection_reason": None,
    }
    leave_records[_next_leave_id] = record
    _next_leave_id += 1
    return record


def approve_leave(leave_id: int, approved_by: int) -> dict:
    if leave_id not in leave_records:
        raise ValueError(f"Leave {leave_id} not found")
    record = leave_records[leave_id]
    if record["status"] != "pending":
        raise ValueError("Only pending leaves can be approved")

    _init_balance(record["emp_id"])
    balance = leave_balances[record["emp_id"]]
    lt = record["leave_type"]
    if balance[lt] < record["days"]:
        raise ValueError("Insufficient leave balance at time of approval")

    balance[lt] -= record["days"]
    record["status"] = "approved"
    record["approved_by"] = approved_by
    return record


def reject_leave(leave_id: int, reason: str) -> dict:
    if leave_id not in leave_records:
        raise ValueError(f"Leave {leave_id} not found")
    record = leave_records[leave_id]
    if record["status"] != "pending":
        raise ValueError("Only pending leaves can be rejected")
    record["status"] = "rejected"
    record["rejection_reason"] = reason
    return record


def get_leave_balance(emp_id: int) -> dict:
    _init_balance(emp_id)
    return {"emp_id": emp_id, "balances": leave_balances[emp_id]}


def check_leave_eligibility(emp_id: int, leave_type: str) -> bool:
    if leave_type not in LEAVE_TYPES:
        return False
    _init_balance(emp_id)
    return leave_balances[emp_id][leave_type] > 0


def get_leave_history(emp_id: int) -> list:
    return [r for r in leave_records.values() if r["emp_id"] == emp_id]
