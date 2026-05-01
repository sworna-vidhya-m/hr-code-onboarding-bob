from app.employee import get_employee

payroll_history: dict = {}


def calculate_monthly_salary(emp_id: int) -> float:
    emp = get_employee(emp_id)
    return round(emp["salary"] / 12, 2)


def apply_deductions(salary: float, deductions: dict) -> float:
    total = sum(deductions.values())
    result = float(salary) - float(total)
    return round(max(result, 0.0), 2)


def calculate_tax(salary: float) -> float:
    annual = salary * 12
    if annual <= 250000:
        tax = 0.0
    elif annual <= 500000:
        tax = (annual - 250000) * 0.05
    elif annual <= 1000000:
        tax = 12500 + (annual - 500000) * 0.20
    else:
        tax = 112500 + (annual - 1000000) * 0.30
    monthly_tax = tax / 12
    return round(monthly_tax, 2)


def generate_payslip(emp_id: int, month: int, year: int) -> dict:
    emp = get_employee(emp_id)
    gross = calculate_monthly_salary(emp_id)
    tax = calculate_tax(gross)
    pf = round(gross * 0.12, 2)
    deductions = {"tax": tax, "pf": pf}
    net = apply_deductions(gross, deductions)

    payslip = {
        "emp_id": emp_id,
        "name": emp["name"],
        "department": emp["department"],
        "month": month,
        "year": year,
        "gross_salary": gross,
        "deductions": deductions,
        "net_salary": net,
    }

    key = f"{emp_id}_{year}_{month:02d}"
    if emp_id not in payroll_history:
        payroll_history[emp_id] = []
    if not any(p["month"] == month and p["year"] == year for p in payroll_history[emp_id]):
        payroll_history[emp_id].append(payslip)

    return payslip


def get_payroll_history(emp_id: int) -> list:
    get_employee(emp_id)
    return payroll_history.get(emp_id, [])


def calculate_bonus(emp_id: int, percentage: float) -> float:
    emp = get_employee(emp_id)
    if percentage < 0:
        raise ValueError("Bonus percentage cannot be negative")
    bonus = emp["salary"] * (percentage / 100)
    return round(bonus, 2)
