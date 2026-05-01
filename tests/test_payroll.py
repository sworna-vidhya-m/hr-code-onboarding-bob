import pytest
from app import employee as emp_module
from app import payroll as payroll_module
from app.payroll import (
    calculate_monthly_salary, apply_deductions,
    calculate_tax, generate_payslip, get_payroll_history, calculate_bonus,
)

SAMPLE = {
    1: {"id": 1, "name": "Raj Kumar", "department": "Engineering", "join_date": "2020-03-15", "salary": 75000, "manager": None},
    2: {"id": 2, "name": "Priya Sharma", "department": "HR", "join_date": "2019-07-01", "salary": 65000, "manager": 1},
    4: {"id": 4, "name": "Meena Iyer", "department": "Engineering", "join_date": "2018-11-20", "salary": 80000, "manager": None},
}


def _reset():
    emp_module.employees.clear()
    emp_module.employees.update({k: dict(v) for k, v in SAMPLE.items()})
    emp_module._next_id = 6
    payroll_module.payroll_history.clear()


class TestCalculateMonthlySalary:
    def setup_method(self):
        _reset()

    def test_basic(self):
        result = calculate_monthly_salary(1)
        assert result == round(75000 / 12, 2)

    def test_higher_salary(self):
        result = calculate_monthly_salary(4)
        assert result == round(80000 / 12, 2)

    def test_nonexistent(self):
        with pytest.raises(ValueError):
            calculate_monthly_salary(999)

    def test_returns_float(self):
        assert isinstance(calculate_monthly_salary(1), float)


class TestApplyDeductions:
    def setup_method(self):
        _reset()

    def test_basic_deduction(self):
        result = apply_deductions(10000, {"tax": 1000, "pf": 500})
        assert result == 8500.0

    def test_no_deductions(self):
        result = apply_deductions(10000, {})
        assert result == 10000.0

    def test_deduction_exceeds_salary(self):
        result = apply_deductions(1000, {"tax": 2000})
        assert result == 0.0

    def test_multiple_deductions(self):
        result = apply_deductions(50000, {"tax": 5000, "pf": 6000, "other": 1000})
        assert result == 38000.0

    def test_returns_float(self):
        assert isinstance(apply_deductions(10000, {"tax": 500}), float)


class TestCalculateTax:
    def setup_method(self):
        _reset()

    def test_no_tax_below_250k_annual(self):
        monthly = 250000 / 12
        assert calculate_tax(monthly) == 0.0

    def test_tax_250k_to_500k(self):
        monthly = 400000 / 12
        tax = calculate_tax(monthly)
        assert tax > 0

    def test_tax_500k_to_1m(self):
        monthly = 750000 / 12
        tax = calculate_tax(monthly)
        assert tax > calculate_tax(400000 / 12)

    def test_tax_above_1m(self):
        monthly = 1500000 / 12
        tax = calculate_tax(monthly)
        assert tax > calculate_tax(750000 / 12)

    def test_returns_float(self):
        assert isinstance(calculate_tax(10000), float)

    def test_tax_is_monthly(self):
        monthly_tax = calculate_tax(6250)  # annual 75000 < 250000
        assert monthly_tax == 0.0


class TestGeneratePayslip:
    def setup_method(self):
        _reset()

    def test_basic_payslip(self):
        slip = generate_payslip(1, 5, 2026)
        assert slip["emp_id"] == 1
        assert slip["month"] == 5
        assert slip["year"] == 2026
        assert "gross_salary" in slip
        assert "net_salary" in slip
        assert "deductions" in slip

    def test_net_less_than_gross(self):
        slip = generate_payslip(4, 5, 2026)
        assert slip["net_salary"] < slip["gross_salary"]

    def test_deductions_present(self):
        slip = generate_payslip(1, 5, 2026)
        assert "tax" in slip["deductions"]
        assert "pf" in slip["deductions"]

    def test_nonexistent_employee(self):
        with pytest.raises(ValueError):
            generate_payslip(999, 5, 2026)

    def test_payslip_stores_history(self):
        generate_payslip(1, 5, 2026)
        hist = get_payroll_history(1)
        assert len(hist) == 1

    def test_duplicate_payslip_not_stored_twice(self):
        generate_payslip(1, 5, 2026)
        generate_payslip(1, 5, 2026)
        hist = get_payroll_history(1)
        assert len(hist) == 1

    def test_different_months_stored(self):
        generate_payslip(1, 4, 2026)
        generate_payslip(1, 5, 2026)
        hist = get_payroll_history(1)
        assert len(hist) == 2

    def test_name_in_payslip(self):
        slip = generate_payslip(1, 5, 2026)
        assert slip["name"] == "Raj Kumar"


class TestGetPayrollHistory:
    def setup_method(self):
        _reset()

    def test_empty_history(self):
        assert get_payroll_history(1) == []

    def test_history_after_payslip(self):
        generate_payslip(1, 5, 2026)
        generate_payslip(1, 4, 2026)
        hist = get_payroll_history(1)
        assert len(hist) == 2

    def test_nonexistent_employee(self):
        with pytest.raises(ValueError):
            get_payroll_history(999)


class TestCalculateBonus:
    def setup_method(self):
        _reset()

    def test_basic_bonus(self):
        bonus = calculate_bonus(1, 10)
        assert bonus == round(75000 * 0.10, 2)

    def test_zero_bonus(self):
        assert calculate_bonus(1, 0) == 0.0

    def test_negative_percentage(self):
        with pytest.raises(ValueError, match="negative"):
            calculate_bonus(1, -5)

    def test_nonexistent_employee(self):
        with pytest.raises(ValueError):
            calculate_bonus(999, 10)

    def test_returns_float(self):
        assert isinstance(calculate_bonus(1, 5), float)

    def test_high_bonus(self):
        bonus = calculate_bonus(4, 50)
        assert bonus == round(80000 * 0.50, 2)
