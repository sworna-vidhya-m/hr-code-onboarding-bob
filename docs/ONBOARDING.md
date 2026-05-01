# HR Employee Management System — Developer Onboarding Guide

## Project Overview

This is an internal HR portal that manages employees, leave requests, and payroll for the organisation. It is a REST API built with Python FastAPI, backed by in-memory storage (no database), and ships with a single-page HTML frontend.

---

## Architecture

```
Browser (static/index.html)
        |
        | HTTP / JSON
        v
FastAPI (app/main.py)
   |           |           |
   v           v           v
employee.py  leave.py  payroll.py
(in-memory) (in-memory) (in-memory)
```

All data is stored in Python dicts at module level. Restarting the server resets all state to the seeded sample data.

---

## File Structure

```
hr-code-onboarding-bob/
├── .gitignore
├── requirements.txt          # Pinned Python dependencies
├── app/
│   ├── __init__.py
│   ├── employee.py           # Employee data model and business logic
│   ├── leave.py              # Leave management and balance tracking
│   ├── payroll.py            # Salary, tax, deductions, payslip generation
│   └── main.py               # FastAPI app, routes, CORS, static file mount
├── static/
│   └── index.html            # Single-page frontend (HTML/CSS/JS, no frameworks)
├── tests/
│   ├── __init__.py
│   ├── test_employee.py
│   ├── test_leave.py
│   └── test_payroll.py
├── docs/
│   └── ONBOARDING.md         # This file
└── README.md
```

---

## Key Functions

### app/employee.py

| Function | Description |
|---|---|
| `add_employee(name, dept, salary, manager)` | Creates a new employee record with an auto-incremented ID and today as the join date |
| `get_employee(emp_id)` | Returns a single employee dict; raises `ValueError` if not found |
| `list_employees()` | Returns all employees as a list |
| `update_salary(emp_id, new_salary)` | Updates salary in place; rejects negative values |
| `calculate_experience_years(emp_id)` | Returns full years since join_date using integer division |
| `get_employees_by_department(dept)` | Case-insensitive department filter |

### app/leave.py

| Function | Description |
|---|---|
| `apply_leave(emp_id, leave_type, days, reason)` | Creates a pending leave record; validates type and balance |
| `approve_leave(leave_id, approved_by)` | Transitions to approved and deducts from balance |
| `reject_leave(leave_id, reason)` | Transitions to rejected; balance is not affected |
| `get_leave_balance(emp_id)` | Returns remaining days per leave type; initialises defaults on first call |
| `check_leave_eligibility(emp_id, leave_type)` | Returns True if any balance remains for the type |
| `get_leave_history(emp_id)` | Returns all leave records for the employee |

Leave type entitlements: `annual=18`, `sick=10`, `maternity=182`, `paternity=5`.

### app/payroll.py

| Function | Description |
|---|---|
| `calculate_monthly_salary(emp_id)` | `annual_salary / 12`, rounded to 2 decimal places |
| `apply_deductions(salary, deductions)` | Subtracts all values in the deductions dict; floors at 0 |
| `calculate_tax(salary)` | Applies Indian income-tax slabs (see Business Rules below) |
| `generate_payslip(emp_id, month, year)` | Builds a payslip dict and appends to history (idempotent per month/year) |
| `get_payroll_history(emp_id)` | Returns all generated payslips for the employee |
| `calculate_bonus(emp_id, percentage)` | `annual_salary * percentage / 100`; rejects negative percentages |

---

## How to Run Locally

**1. Create and activate the virtual environment:**

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

**2. Install dependencies:**

```bash
pip install -r requirements.txt
```

**3. Start the server:**

```bash
uvicorn app.main:app --reload
```

The API is at `http://localhost:8000` and the frontend at `http://localhost:8000/`.

Interactive API docs: `http://localhost:8000/docs`

**4. Run tests:**

```bash
pytest tests/
```

---

## Business Rules

### Tax Slabs (Indian Income Tax — Annual Salary)

| Annual Income Range | Tax Rate |
|---|---|
| Up to ₹2,50,000 | Nil |
| ₹2,50,001 – ₹5,00,000 | 5% on amount above ₹2,50,000 |
| ₹5,00,001 – ₹10,00,000 | ₹12,500 + 20% on amount above ₹5,00,000 |
| Above ₹10,00,000 | ₹1,12,500 + 30% on amount above ₹10,00,000 |

Tax is calculated annually then divided by 12 for monthly deduction.

### PF Deduction

- 12% of monthly gross salary is deducted as Provident Fund (PF).

### Leave Rules

- Leave balances initialise to the type entitlement on first access.
- Applying leave checks balance at application time; approval re-checks and deducts.
- Rejecting a leave does **not** deduct from the balance.
- Only `pending` leaves can be approved or rejected.

### Salary Updates

- Salary cannot be set to a negative value.
- Changes take effect immediately in the in-memory store.

---

## API Endpoints Reference

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Service health check |
| `GET` | `/employees` | List all employees |
| `POST` | `/employees` | Add a new employee |
| `GET` | `/employees/{emp_id}` | Get a single employee |
| `GET` | `/leave/{emp_id}` | Get leave balance and history |
| `POST` | `/leave/apply` | Apply for leave |
| `POST` | `/leave/approve` | Approve a pending leave |
| `GET` | `/payroll/{emp_id}` | Get payroll summary |
| `GET` | `/payroll/{emp_id}/payslip` | Generate/fetch a payslip (`?month=5&year=2026`) |
| `GET` | `/` | Serves the frontend HTML |
| `GET` | `/docs` | FastAPI auto-generated API documentation |

### Request Bodies

**POST /employees**
```json
{ "name": "string", "department": "string", "salary": 70000, "manager": 1 }
```

**POST /leave/apply**
```json
{ "emp_id": 1, "leave_type": "annual", "days": 3, "reason": "string" }
```

**POST /leave/approve**
```json
{ "leave_id": 1, "approved_by": 2 }
```

---

## Sample Data

The system starts with five seeded employees:

| ID | Name | Department | Annual Salary |
|---|---|---|---|
| 1 | Raj Kumar | Engineering | ₹75,000 |
| 2 | Priya Sharma | HR | ₹65,000 |
| 3 | Arun Patel | Finance | ₹70,000 |
| 4 | Meena Iyer | Engineering | ₹80,000 |
| 5 | Suresh Babu | Operations | ₹60,000 |
