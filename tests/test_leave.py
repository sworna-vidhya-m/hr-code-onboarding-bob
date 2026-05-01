import pytest
from app import leave as leave_module
from app.leave import (
    apply_leave, approve_leave, reject_leave,
    get_leave_balance, check_leave_eligibility, get_leave_history,
    LEAVE_TYPES,
)


def _reset():
    leave_module.leave_records.clear()
    leave_module.leave_balances.clear()
    leave_module._next_leave_id = 1


class TestGetLeaveBalance:
    def setup_method(self):
        _reset()

    def test_initial_balance(self):
        bal = get_leave_balance(10)
        assert bal["balances"]["annual"] == LEAVE_TYPES["annual"]
        assert bal["balances"]["sick"] == LEAVE_TYPES["sick"]
        assert bal["balances"]["maternity"] == LEAVE_TYPES["maternity"]
        assert bal["balances"]["paternity"] == LEAVE_TYPES["paternity"]

    def test_balance_has_emp_id(self):
        bal = get_leave_balance(5)
        assert bal["emp_id"] == 5


class TestCheckLeaveEligibility:
    def setup_method(self):
        _reset()

    def test_eligible_annual(self):
        assert check_leave_eligibility(1, "annual") is True

    def test_eligible_sick(self):
        assert check_leave_eligibility(1, "sick") is True

    def test_invalid_leave_type(self):
        assert check_leave_eligibility(1, "vacation") is False

    def test_not_eligible_after_zero_balance(self):
        leave_module.leave_balances[99] = {"annual": 0, "sick": 10, "maternity": 182, "paternity": 5}
        assert check_leave_eligibility(99, "annual") is False


class TestApplyLeave:
    def setup_method(self):
        _reset()

    def test_apply_annual(self):
        r = apply_leave(1, "annual", 3, "Family trip")
        assert r["emp_id"] == 1
        assert r["leave_type"] == "annual"
        assert r["days"] == 3
        assert r["status"] == "pending"
        assert r["leave_id"] == 1

    def test_apply_sick_leave(self):
        r = apply_leave(2, "sick", 2, "Fever")
        assert r["leave_type"] == "sick"

    def test_apply_invalid_type(self):
        with pytest.raises(ValueError, match="Invalid leave type"):
            apply_leave(1, "vacation", 2, "Holiday")

    def test_apply_zero_days(self):
        with pytest.raises(ValueError, match="positive"):
            apply_leave(1, "annual", 0, "test")

    def test_apply_negative_days(self):
        with pytest.raises(ValueError):
            apply_leave(1, "annual", -1, "test")

    def test_apply_increments_id(self):
        r1 = apply_leave(1, "annual", 1, "Day off")
        r2 = apply_leave(2, "sick", 1, "Ill")
        assert r2["leave_id"] == r1["leave_id"] + 1

    def test_apply_no_balance(self):
        leave_module.leave_balances[50] = {"annual": 0, "sick": 10, "maternity": 182, "paternity": 5}
        with pytest.raises(ValueError, match="Insufficient"):
            apply_leave(50, "annual", 1, "test")

    def test_apply_sets_applied_on(self):
        r = apply_leave(1, "annual", 1, "test")
        assert r["applied_on"] is not None


class TestApproveLeave:
    def setup_method(self):
        _reset()

    def test_approve_pending(self):
        r = apply_leave(1, "annual", 2, "Trip")
        approved = approve_leave(r["leave_id"], 99)
        assert approved["status"] == "approved"
        assert approved["approved_by"] == 99

    def test_approve_deducts_balance(self):
        r = apply_leave(1, "annual", 5, "Vacation")
        initial = get_leave_balance(1)["balances"]["annual"]
        approve_leave(r["leave_id"], 99)
        final = get_leave_balance(1)["balances"]["annual"]
        assert final == initial - 5

    def test_approve_nonexistent(self):
        with pytest.raises(ValueError, match="not found"):
            approve_leave(999, 1)

    def test_approve_already_approved(self):
        r = apply_leave(1, "annual", 1, "test")
        approve_leave(r["leave_id"], 1)
        with pytest.raises(ValueError, match="pending"):
            approve_leave(r["leave_id"], 1)


class TestRejectLeave:
    def setup_method(self):
        _reset()

    def test_reject_pending(self):
        r = apply_leave(1, "annual", 2, "Trip")
        rej = reject_leave(r["leave_id"], "Not approved this period")
        assert rej["status"] == "rejected"
        assert rej["rejection_reason"] == "Not approved this period"

    def test_reject_nonexistent(self):
        with pytest.raises(ValueError, match="not found"):
            reject_leave(999, "reason")

    def test_reject_already_rejected(self):
        r = apply_leave(1, "sick", 1, "test")
        reject_leave(r["leave_id"], "reason")
        with pytest.raises(ValueError, match="pending"):
            reject_leave(r["leave_id"], "again")

    def test_reject_does_not_deduct_balance(self):
        r = apply_leave(1, "annual", 5, "test")
        initial = get_leave_balance(1)["balances"]["annual"]
        reject_leave(r["leave_id"], "reason")
        final = get_leave_balance(1)["balances"]["annual"]
        assert final == initial


class TestGetLeaveHistory:
    def setup_method(self):
        _reset()

    def test_empty_history(self):
        assert get_leave_history(100) == []

    def test_history_after_apply(self):
        apply_leave(10, "annual", 1, "Day off")
        apply_leave(10, "sick", 2, "Ill")
        hist = get_leave_history(10)
        assert len(hist) == 2

    def test_history_only_own_records(self):
        apply_leave(1, "annual", 1, "Mine")
        apply_leave(2, "sick", 1, "Theirs")
        hist = get_leave_history(1)
        assert all(r["emp_id"] == 1 for r in hist)
