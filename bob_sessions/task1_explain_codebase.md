**User:**

<task>
@app/main.py @app/employee.py 
@app/leave.py @app/payroll.py

A new developer just joined our team today.
Explain this entire codebase to them:
1. What does this system do?
2. How do the 4 files connect to each other?
3. What are the most important functions?
4. What business rules are embedded in the code?
5. Where should a new developer start reading?
</task>
<environment_details>
# VSCode Visible Files
app/employee.py

# VSCode Open Tabs
app/employee.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-01T17:47:42.830Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>


# Current Workspace Directory (/Users/swornamacair/Documents/IBM_Hackathon/hr-code-onboarding-bob) Files
.gitignore
README.md
requirements.txt
app/
app/__init__.py
app/employee.py
app/leave.py
app/main.py
app/payroll.py
bob_sessions/
docs/
docs/ONBOARDING.md
static/
static/index.html
tests/
tests/__init__.py
tests/test_employee.py
tests/test_leave.py
tests/test_payroll.py
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll analyze this codebase to provide a comprehensive onboarding guide for the new developer. Let me start by reading all four files to understand the system.

<read_file>
<args>
  <file>
    <path>app/main.py</path>
  </file>
  <file>
    <path>app/employee.py</path>
  </file>
  <file>
    <path>app/leave.py</path>
  </file>
  <file>
    <path>app/payroll.py</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 4 files] Result:
<files>
<file><path>app/main.py</path>
<content lines="1-127">
  1 | from fastapi import FastAPI, HTTPException
  2 | from fastapi.middleware.cors import CORSMiddleware
  3 | from fastapi.staticfiles import StaticFiles
  4 | from fastapi.responses import FileResponse
  5 | from pydantic import BaseModel
  6 | from typing import Optional
  7 | from datetime import date
  8 | import os
  9 | 
 10 | from app import employee, leave, payroll
 11 | 
 12 | app = FastAPI(title="HR Employee Management System")
 13 | 
 14 | app.add_middleware(
 15 |     CORSMiddleware,
 16 |     allow_origins=["*"],
 17 |     allow_methods=["*"],
 18 |     allow_headers=["*"],
 19 | )
 20 | 
 21 | static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
 22 | app.mount("/static", StaticFiles(directory=static_dir), name="static")
 23 | 
 24 | 
 25 | class EmployeeCreate(BaseModel):
 26 |     name: str
 27 |     department: str
 28 |     salary: float
 29 |     manager: Optional[int] = None
 30 | 
 31 | 
 32 | class LeaveApply(BaseModel):
 33 |     emp_id: int
 34 |     leave_type: str
 35 |     days: int
 36 |     reason: str
 37 | 
 38 | 
 39 | class LeaveApprove(BaseModel):
 40 |     leave_id: int
 41 |     approved_by: int
 42 | 
 43 | 
 44 | @app.get("/health")
 45 | def health():
 46 |     return {"status": "ok", "service": "HR Employee Management System"}
 47 | 
 48 | 
 49 | @app.get("/employees")
 50 | def list_employees():
 51 |     return employee.list_employees()
 52 | 
 53 | 
 54 | @app.post("/employees", status_code=201)
 55 | def create_employee(data: EmployeeCreate):
 56 |     return employee.add_employee(data.name, data.department, data.salary, data.manager)
 57 | 
 58 | 
 59 | @app.get("/employees/{emp_id}")
 60 | def get_employee(emp_id: int):
 61 |     try:
 62 |         return employee.get_employee(emp_id)
 63 |     except ValueError as e:
 64 |         raise HTTPException(status_code=404, detail=str(e))
 65 | 
 66 | 
 67 | @app.get("/leave/{emp_id}")
 68 | def leave_balance(emp_id: int):
 69 |     try:
 70 |         employee.get_employee(emp_id)
 71 |     except ValueError as e:
 72 |         raise HTTPException(status_code=404, detail=str(e))
 73 |     balance = leave.get_leave_balance(emp_id)
 74 |     history = leave.get_leave_history(emp_id)
 75 |     return {**balance, "history": history}
 76 | 
 77 | 
 78 | @app.post("/leave/apply")
 79 | def apply_leave(data: LeaveApply):
 80 |     try:
 81 |         employee.get_employee(data.emp_id)
 82 |         return leave.apply_leave(data.emp_id, data.leave_type, data.days, data.reason)
 83 |     except ValueError as e:
 84 |         raise HTTPException(status_code=400, detail=str(e))
 85 | 
 86 | 
 87 | @app.post("/leave/approve")
 88 | def approve_leave(data: LeaveApprove):
 89 |     try:
 90 |         return leave.approve_leave(data.leave_id, data.approved_by)
 91 |     except ValueError as e:
 92 |         raise HTTPException(status_code=400, detail=str(e))
 93 | 
 94 | 
 95 | @app.get("/payroll/{emp_id}")
 96 | def payroll_info(emp_id: int):
 97 |     try:
 98 |         emp = employee.get_employee(emp_id)
 99 |         gross = payroll.calculate_monthly_salary(emp_id)
100 |         tax = payroll.calculate_tax(gross)
101 |         pf = round(gross * 0.12, 2)
102 |         net = payroll.apply_deductions(gross, {"tax": tax, "pf": pf})
103 |         return {
104 |             "emp_id": emp_id,
105 |             "name": emp["name"],
106 |             "annual_salary": emp["salary"],
107 |             "monthly_gross": gross,
108 |             "monthly_tax": tax,
109 |             "monthly_pf": pf,
110 |             "monthly_net": net,
111 |             "experience_years": employee.calculate_experience_years(emp_id),
112 |         }
113 |     except ValueError as e:
114 |         raise HTTPException(status_code=404, detail=str(e))
115 | 
116 | 
117 | @app.get("/payroll/{emp_id}/payslip")
118 | def get_payslip(emp_id: int, month: int = date.today().month, year: int = date.today().year):
119 |     try:
120 |         return payroll.generate_payslip(emp_id, month, year)
121 |     except ValueError as e:
122 |         raise HTTPException(status_code=404, detail=str(e))
123 | 
124 | 
125 | @app.get("/")
126 | def index():
127 |     return FileResponse(os.path.join(static_dir, "index.html"))
</content>
</file>
<file><path>app/employee.py</path>
<content lines="1-92">
 1 | from datetime import date, datetime
 2 | from typing import Optional
 3 | 
 4 | employees: dict = {
 5 |     1: {
 6 |         "id": 1,
 7 |         "name": "Raj Kumar",
 8 |         "department": "Engineering",
 9 |         "join_date": "2020-03-15",
10 |         "salary": 75000,
11 |         "manager": None,
12 |     },
13 |     2: {
14 |         "id": 2,
15 |         "name": "Priya Sharma",
16 |         "department": "HR",
17 |         "join_date": "2019-07-01",
18 |         "salary": 65000,
19 |         "manager": 1,
20 |     },
21 |     3: {
22 |         "id": 3,
23 |         "name": "Arun Patel",
24 |         "department": "Finance",
25 |         "join_date": "2021-01-10",
26 |         "salary": 70000,
27 |         "manager": 1,
28 |     },
29 |     4: {
30 |         "id": 4,
31 |         "name": "Meena Iyer",
32 |         "department": "Engineering",
33 |         "join_date": "2018-11-20",
34 |         "salary": 80000,
35 |         "manager": None,
36 |     },
37 |     5: {
38 |         "id": 5,
39 |         "name": "Suresh Babu",
40 |         "department": "Operations",
41 |         "join_date": "2022-06-05",
42 |         "salary": 60000,
43 |         "manager": 2,
44 |     },
45 | }
46 | 
47 | _next_id: int = 6
48 | 
49 | 
50 | def add_employee(name: str, department: str, salary: float, manager: Optional[int] = None) -> dict:
51 |     global _next_id
52 |     emp = {
53 |         "id": _next_id,
54 |         "name": name,
55 |         "department": department,
56 |         "join_date": date.today().isoformat(),
57 |         "salary": salary,
58 |         "manager": manager,
59 |     }
60 |     employees[_next_id] = emp
61 |     _next_id += 1
62 |     return emp
63 | 
64 | 
65 | def get_employee(emp_id: int) -> dict:
66 |     if emp_id not in employees:
67 |         raise ValueError(f"Employee {emp_id} not found")
68 |     return employees[emp_id]
69 | 
70 | 
71 | def list_employees() -> list:
72 |     return list(employees.values())
73 | 
74 | 
75 | def update_salary(emp_id: int, new_salary: float) -> dict:
76 |     if emp_id not in employees:
77 |         raise ValueError(f"Employee {emp_id} not found")
78 |     if new_salary < 0:
79 |         raise ValueError("Salary cannot be negative")
80 |     employees[emp_id]["salary"] = new_salary
81 |     return employees[emp_id]
82 | 
83 | 
84 | def calculate_experience_years(emp_id: int) -> int:
85 |     emp = get_employee(emp_id)
86 |     join = datetime.strptime(emp["join_date"], "%Y-%m-%d").date()
87 |     today = date.today()
88 |     return (today - join).days // 365
89 | 
90 | 
91 | def get_employees_by_department(department: str) -> list:
92 |     return [e for e in employees.values() if e["department"].lower() == department.lower()]
</content>
</file>
<file><path>app/leave.py</path>
<content lines="1-89">
 1 | from datetime import date
 2 | from typing import Optional
 3 | 
 4 | LEAVE_TYPES = {
 5 |     "annual": 18,
 6 |     "sick": 10,
 7 |     "maternity": 182,
 8 |     "paternity": 5,
 9 | }
10 | 
11 | leave_records: dict = {}
12 | leave_balances: dict = {}
13 | _next_leave_id: int = 1
14 | 
15 | 
16 | def _init_balance(emp_id: int) -> None:
17 |     if emp_id not in leave_balances:
18 |         leave_balances[emp_id] = {lt: days for lt, days in LEAVE_TYPES.items()}
19 | 
20 | 
21 | def apply_leave(emp_id: int, leave_type: str, days: int, reason: str) -> dict:
22 |     global _next_leave_id
23 |     if leave_type not in LEAVE_TYPES:
24 |         raise ValueError(f"Invalid leave type: {leave_type}")
25 |     if days <= 0:
26 |         raise ValueError("Days must be positive")
27 |     if not check_leave_eligibility(emp_id, leave_type):
28 |         raise ValueError(f"Insufficient {leave_type} leave balance")
29 | 
30 |     record = {
31 |         "leave_id": _next_leave_id,
32 |         "emp_id": emp_id,
33 |         "leave_type": leave_type,
34 |         "days": days,
35 |         "reason": reason,
36 |         "status": "pending",
37 |         "applied_on": date.today().isoformat(),
38 |         "approved_by": None,
39 |         "rejection_reason": None,
40 |     }
41 |     leave_records[_next_leave_id] = record
42 |     _next_leave_id += 1
43 |     return record
44 | 
45 | 
46 | def approve_leave(leave_id: int, approved_by: int) -> dict:
47 |     if leave_id not in leave_records:
48 |         raise ValueError(f"Leave {leave_id} not found")
49 |     record = leave_records[leave_id]
50 |     if record["status"] != "pending":
51 |         raise ValueError("Only pending leaves can be approved")
52 | 
53 |     _init_balance(record["emp_id"])
54 |     balance = leave_balances[record["emp_id"]]
55 |     lt = record["leave_type"]
56 |     if balance[lt] < record["days"]:
57 |         raise ValueError("Insufficient leave balance at time of approval")
58 | 
59 |     balance[lt] -= record["days"]
60 |     record["status"] = "approved"
61 |     record["approved_by"] = approved_by
62 |     return record
63 | 
64 | 
65 | def reject_leave(leave_id: int, reason: str) -> dict:
66 |     if leave_id not in leave_records:
67 |         raise ValueError(f"Leave {leave_id} not found")
68 |     record = leave_records[leave_id]
69 |     if record["status"] != "pending":
70 |         raise ValueError("Only pending leaves can be rejected")
71 |     record["status"] = "rejected"
72 |     record["rejection_reason"] = reason
73 |     return record
74 | 
75 | 
76 | def get_leave_balance(emp_id: int) -> dict:
77 |     _init_balance(emp_id)
78 |     return {"emp_id": emp_id, "balances": leave_balances[emp_id]}
79 | 
80 | 
81 | def check_leave_eligibility(emp_id: int, leave_type: str) -> bool:
82 |     if leave_type not in LEAVE_TYPES:
83 |         return False
84 |     _init_balance(emp_id)
85 |     return leave_balances[emp_id][leave_type] > 0
86 | 
87 | 
88 | def get_leave_history(emp_id: int) -> list:
89 |     return [r for r in leave_records.values() if r["emp_id"] == emp_id]
</content>
</file>
<file><path>app/payroll.py</path>
<content lines="1-69">
 1 | from app.employee import get_employee
 2 | 
 3 | payroll_history: dict = {}
 4 | 
 5 | 
 6 | def calculate_monthly_salary(emp_id: int) -> float:
 7 |     emp = get_employee(emp_id)
 8 |     return round(emp["salary"] / 12, 2)
 9 | 
10 | 
11 | def apply_deductions(salary: float, deductions: dict) -> float:
12 |     total = sum(deductions.values())
13 |     result = float(salary) - float(total)
14 |     return round(max(result, 0.0), 2)
15 | 
16 | 
17 | def calculate_tax(salary: float) -> float:
18 |     annual = salary * 12
19 |     if annual <= 250000:
20 |         tax = 0.0
21 |     elif annual <= 500000:
22 |         tax = (annual - 250000) * 0.05
23 |     elif annual <= 1000000:
24 |         tax = 12500 + (annual - 500000) * 0.20
25 |     else:
26 |         tax = 112500 + (annual - 1000000) * 0.30
27 |     monthly_tax = tax / 12
28 |     return round(monthly_tax, 2)
29 | 
30 | 
31 | def generate_payslip(emp_id: int, month: int, year: int) -> dict:
32 |     emp = get_employee(emp_id)
33 |     gross = calculate_monthly_salary(emp_id)
34 |     tax = calculate_tax(gross)
35 |     pf = round(gross * 0.12, 2)
36 |     deductions = {"tax": tax, "pf": pf}
37 |     net = apply_deductions(gross, deductions)
38 | 
39 |     payslip = {
40 |         "emp_id": emp_id,
41 |         "name": emp["name"],
42 |         "department": emp["department"],
43 |         "month": month,
44 |         "year": year,
45 |         "gross_salary": gross,
46 |         "deductions": deductions,
47 |         "net_salary": net,
48 |     }
49 | 
50 |     key = f"{emp_id}_{year}_{month:02d}"
51 |     if emp_id not in payroll_history:
52 |         payroll_history[emp_id] = []
53 |     if not any(p["month"] == month and p["year"] == year for p in payroll_history[emp_id]):
54 |         payroll_history[emp_id].append(payslip)
55 | 
56 |     return payslip
57 | 
58 | 
59 | def get_payroll_history(emp_id: int) -> list:
60 |     get_employee(emp_id)
61 |     return payroll_history.get(emp_id, [])
62 | 
63 | 
64 | def calculate_bonus(emp_id: int, percentage: float) -> float:
65 |     emp = get_employee(emp_id)
66 |     if percentage < 0:
67 |         raise ValueError("Bonus percentage cannot be negative")
68 |     bonus = emp["salary"] * (percentage / 100)
69 |     return round(bonus, 2)
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
app/employee.py

# VSCode Open Tabs
app/employee.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-01T17:47:54.752Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.02

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

# HR Employee Management System - Onboarding Guide

Welcome to the team! Let me walk you through this codebase systematically.

## 1. What Does This System Do?

This is an **HR Employee Management System** built with FastAPI that handles three core HR functions:

- **Employee Management**: Track employee records, departments, salaries, and reporting structures
- **Leave Management**: Handle leave applications, approvals, and balance tracking
- **Payroll Processing**: Calculate salaries, taxes, deductions, and generate payslips

The system provides a REST API backend with a web interface for HR operations.

## 2. How the 4 Files Connect

```mermaid
graph TD
    A[main.py<br/>FastAPI Routes] --> B[employee.py<br/>Employee Data]
    A --> C[leave.py<br/>Leave Management]
    A --> D[payroll.py<br/>Payroll Calculations]
    D --> B
    C -.validates.-> B
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#e8f5e9
    style D fill:#fce4ec
```

### Connection Flow:

**[`main.py`](app/main.py:1)** - The API Gateway
- Defines all HTTP endpoints (GET/POST routes)
- Imports and orchestrates the other three modules
- Handles request validation via Pydantic models
- Converts business logic errors into HTTP responses

**[`employee.py`](app/employee.py:1)** - The Foundation
- Stores employee data in an in-memory dictionary
- Provides CRUD operations for employee records
- Used by both [`leave.py`](app/leave.py:1) and [`payroll.py`](app/payroll.py:1)

**[`leave.py`](app/leave.py:1)** - Leave System (Independent)
- Manages leave applications and approvals
- Tracks leave balances per employee
- Validates against employee existence via [`main.py`](app/main.py:70-72)

**[`payroll.py`](app/payroll.py:1)** - Payroll System (Depends on Employee)
- Directly imports [`get_employee()`](app/employee.py:65) from [`employee.py`](app/employee.py:1)
- Calculates salaries, taxes, and generates payslips
- Maintains payroll history

## 3. Most Important Functions

### Core Employee Functions ([`employee.py`](app/employee.py:1))

| Function | Purpose | Line |
|----------|---------|------|
| [`get_employee(emp_id)`](app/employee.py:65) | Retrieves employee by ID - **used everywhere** | 65 |
| [`add_employee()`](app/employee.py:50) | Creates new employee records | 50 |
| [`calculate_experience_years()`](app/employee.py:84) | Calculates tenure from join date | 84 |

### Leave Management ([`leave.py`](app/leave.py:1))

| Function | Purpose | Line |
|----------|---------|------|
| [`apply_leave()`](app/leave.py:21) | Creates leave request with validation | 21 |
| [`approve_leave()`](app/leave.py:46) | Approves leave and deducts balance | 46 |
| [`get_leave_balance()`](app/leave.py:76) | Returns available leave days | 76 |

### Payroll Calculations ([`payroll.py`](app/payroll.py:1))

| Function | Purpose | Line |
|----------|---------|------|
| [`calculate_tax()`](app/payroll.py:17) | Applies Indian tax slabs | 17 |
| [`generate_payslip()`](app/payroll.py:31) | Creates complete payslip with all deductions | 31 |
| [`apply_deductions()`](app/payroll.py:11) | Subtracts tax/PF from gross salary | 11 |

## 4. Business Rules Embedded in Code

### Leave Rules ([`leave.py`](app/leave.py:4-9))
```python
LEAVE_TYPES = {
    "annual": 18,      # 18 days annual leave
    "sick": 10,        # 10 days sick leave
    "maternity": 182,  # ~6 months maternity
    "paternity": 5     # 5 days paternity
}
```
- Leave must be applied before approval
- Balance checked at both application and approval time
- Only "pending" leaves can be approved/rejected

### Tax Calculation ([`payroll.py`](app/payroll.py:17-28))
Indian tax slab system:
- ≤₹2.5L: 0% tax
- ₹2.5L-₹5L: 5% on amount above ₹2.5L
- ₹5L-₹10L: ₹12,500 + 20% on amount above ₹5L
- >₹10L: ₹1,12,500 + 30% on amount above ₹10L

### Payroll Rules ([`payroll.py`](app/payroll.py:35))
- **PF (Provident Fund)**: Fixed at 12% of gross salary
- **Monthly salary**: Annual salary ÷ 12
- **Net salary**: Cannot be negative (floor at 0)

### Employee Rules ([`employee.py`](app/employee.py:78-79))
- Salary cannot be negative
- Join date auto-set to today for new employees
- Manager field is optional (for top-level employees)

## 5. Where Should a New Developer Start Reading?

### Recommended Reading Order:

**Step 1: Start with [`employee.py`](app/employee.py:1)** (15 minutes)
- Simplest module with no dependencies
- Understand the data structure (lines 4-45)
- Review basic CRUD operations
- **Key insight**: Everything revolves around the `employees` dictionary

**Step 2: Read [`main.py`](app/main.py:1)** (20 minutes)
- See how the API is structured
- Understand Pydantic models (lines 25-42)
- Follow the endpoint patterns:
  - Employee endpoints (lines 49-64)
  - Leave endpoints (lines 67-92)
  - Payroll endpoints (lines 95-122)
- **Key insight**: [`main.py`](app/main.py:1) validates and routes, business logic lives elsewhere

**Step 3: Explore [`payroll.py`](app/payroll.py:1)** (15 minutes)
- See how it imports from [`employee.py`](app/employee.py:1) (line 1)
- Understand the tax calculation logic
- Notice the payroll history tracking
- **Key insight**: Direct dependency on employee module

**Step 4: Study [`leave.py`](app/leave.py:1)** (15 minutes)
- Most complex business logic
- Understand the state machine (pending → approved/rejected)
- See the balance initialization pattern
- **Key insight**: Validates employee existence through [`main.py`](app/main.py:1), not directly

### Quick Start Commands:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload

# Access the API
# Browser: http://localhost:8000
# API docs: http://localhost:8000/docs
```

### Key Architectural Patterns to Notice:

1. **In-memory storage**: All data stored in dictionaries (no database yet)
2. **Global state**: Uses module-level variables for data persistence
3. **Error handling**: Raises `ValueError` for business logic errors, converted to HTTP errors in [`main.py`](app/main.py:1)
4. **Separation of concerns**: Each module handles one domain
5. **Validation layers**: Pydantic models in [`main.py`](app/main.py:1), business rules in domain modules

### Testing:
Check [`tests/`](tests/) directory for examples of how each module is tested:
- [`test_employee.py`](tests/test_employee.py:1)
- [`test_leave.py`](tests/test_leave.py:1)
- [`test_payroll.py`](tests/test_payroll.py:1)

---

**Pro tip**: Open [`app/main.py`](app/main.py:1) and the API docs (`/docs` endpoint) side-by-side to see how HTTP requests map to function calls. This will help you understand the complete request flow!

---

**User:**

[ERROR] You did not use a tool in your previous response! Please retry with a tool use.

# Reminder: Instructions for Tool Use

Tool uses are formatted using XML-style tags. The tool name itself becomes the XML tag name. Each parameter is enclosed within its own set of tags. Here's the structure:

<actual_tool_name>
<parameter1_name>value1</parameter1_name>
<parameter2_name>value2</parameter2_name>
...
</actual_tool_name>

For example, to use the attempt_completion tool:

<attempt_completion>
<result>
I have completed the task...
</result>
</attempt_completion>

Always use the actual tool name as the XML tag name for proper parsing and execution.

# Next Steps

If you have completed the user's task, use the attempt_completion tool.
If you require additional information from the user, use the ask_followup_question tool.
Otherwise, if you have not completed the task and do not need additional information, then proceed with the next step of the task.
(This is an automated message, so do not respond to it conversationally.)
<environment_details>
# VSCode Visible Files
app/employee.py

# VSCode Open Tabs
app/employee.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-01T17:48:29.659Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.07

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
# HR Employee Management System - Onboarding Guide

Welcome to the team! Let me walk you through this codebase systematically.

## 1. What Does This System Do?

This is an **HR Employee Management System** built with FastAPI that handles three core HR functions:

- **Employee Management**: Track employee records, departments, salaries, and reporting structures
- **Leave Management**: Handle leave applications, approvals, and balance tracking
- **Payroll Processing**: Calculate salaries, taxes, deductions, and generate payslips

The system provides a REST API backend with a web interface for HR operations.

## 2. How the 4 Files Connect

```mermaid
graph TD
    A[main.py<br/>FastAPI Routes] --> B[employee.py<br/>Employee Data]
    A --> C[leave.py<br/>Leave Management]
    A --> D[payroll.py<br/>Payroll Calculations]
    D --> B
    C -.validates.-> B
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#e8f5e9
    style D fill:#fce4ec
```

### Connection Flow:

**[`main.py`](app/main.py:1)** - The API Gateway
- Defines all HTTP endpoints (GET/POST routes)
- Imports and orchestrates the other three modules
- Handles request validation via Pydantic models
- Converts business logic errors into HTTP responses

**[`employee.py`](app/employee.py:1)** - The Foundation
- Stores employee data in an in-memory dictionary
- Provides CRUD operations for employee records
- Used by both [`leave.py`](app/leave.py:1) and [`payroll.py`](app/payroll.py:1)

**[`leave.py`](app/leave.py:1)** - Leave System (Independent)
- Manages leave applications and approvals
- Tracks leave balances per employee
- Validates against employee existence via [`main.py`](app/main.py:70-72)

**[`payroll.py`](app/payroll.py:1)** - Payroll System (Depends on Employee)
- Directly imports [`get_employee()`](app/employee.py:65) from [`employee.py`](app/employee.py:1)
- Calculates salaries, taxes, and generates payslips
- Maintains payroll history

## 3. Most Important Functions

### Core Employee Functions ([`employee.py`](app/employee.py:1))

| Function | Purpose | Line |
|----------|---------|------|
| [`get_employee(emp_id)`](app/employee.py:65) | Retrieves employee by ID - **used everywhere** | 65 |
| [`add_employee()`](app/employee.py:50) | Creates new employee records | 50 |
| [`calculate_experience_years()`](app/employee.py:84) | Calculates tenure from join date | 84 |

### Leave Management ([`leave.py`](app/leave.py:1))

| Function | Purpose | Line |
|----------|---------|------|
| [`apply_leave()`](app/leave.py:21) | Creates leave request with validation | 21 |
| [`approve_leave()`](app/leave.py:46) | Approves leave and deducts balance | 46 |
| [`get_leave_balance()`](app/leave.py:76) | Returns available leave days | 76 |

### Payroll Calculations ([`payroll.py`](app/payroll.py:1))

| Function | Purpose | Line |
|----------|---------|------|
| [`calculate_tax()`](app/payroll.py:17) | Applies Indian tax slabs | 17 |
| [`generate_payslip()`](app/payroll.py:31) | Creates complete payslip with all deductions | 31 |
| [`apply_deductions()`](app/payroll.py:11) | Subtracts tax/PF from gross salary | 11 |

## 4. Business Rules Embedded in Code

### Leave Rules ([`leave.py`](app/leave.py:4-9))
```python
LEAVE_TYPES = {
    "annual": 18,      # 18 days annual leave
    "sick": 10,        # 10 days sick leave
    "maternity": 182,  # ~6 months maternity
    "paternity": 5     # 5 days paternity
}
```
- Leave must be applied before approval
- Balance checked at both application and approval time
- Only "pending" leaves can be approved/rejected

### Tax Calculation ([`payroll.py`](app/payroll.py:17-28))
Indian tax slab system:
- ≤₹2.5L: 0% tax
- ₹2.5L-₹5L: 5% on amount above ₹2.5L
- ₹5L-₹10L: ₹12,500 + 20% on amount above ₹5L
- >₹10L: ₹1,12,500 + 30% on amount above ₹10L

### Payroll Rules ([`payroll.py`](app/payroll.py:35))
- **PF (Provident Fund)**: Fixed at 12% of gross salary
- **Monthly salary**: Annual salary ÷ 12
- **Net salary**: Cannot be negative (floor at 0)

### Employee Rules ([`employee.py`](app/employee.py:78-79))
- Salary cannot be negative
- Join date auto-set to today for new employees
- Manager field is optional (for top-level employees)

## 5. Where Should a New Developer Start Reading?

### Recommended Reading Order:

**Step 1: Start with [`employee.py`](app/employee.py:1)** (15 minutes)
- Simplest module with no dependencies
- Understand the data structure (lines 4-45)
- Review basic CRUD operations
- **Key insight**: Everything revolves around the `employees` dictionary

**Step 2: Read [`main.py`](app/main.py:1)** (20 minutes)
- See how the API is structured
- Understand Pydantic models (lines 25-42)
- Follow the endpoint patterns:
  - Employee endpoints (lines 49-64)
  - Leave endpoints (lines 67-92)
  - Payroll endpoints (lines 95-122)
- **Key insight**: [`main.py`](app/main.py:1) validates and routes, business logic lives elsewhere

**Step 3: Explore [`payroll.py`](app/payroll.py:1)** (15 minutes)
- See how it imports from [`employee.py`](app/employee.py:1) (line 1)
- Understand the tax calculation logic
- Notice the payroll history tracking
- **Key insight**: Direct dependency on employee module

**Step 4: Study [`leave.py`](app/leave.py:1)** (15 minutes)
- Most complex business logic
- Understand the state machine (pending → approved/rejected)
- See the balance initialization pattern
- **Key insight**: Validates employee existence through [`main.py`](app/main.py:1), not directly

### Key Architectural Patterns:

1. **In-memory storage**: All data stored in dictionaries (no database yet)
2. **Global state**: Uses module-level variables for data persistence
3. **Error handling**: Raises `ValueError` for business logic errors, converted to HTTP errors in [`main.py`](app/main.py:1)
4. **Separation of concerns**: Each module handles one domain
5. **Validation layers**: Pydantic models in [`main.py`](app/main.py:1), business rules in domain modules
</result>
</attempt_completion>

