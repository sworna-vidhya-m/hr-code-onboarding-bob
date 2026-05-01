# HR Employee Management System — Developer Onboarding Guide

Welcome to the HR Employee Management System! This guide will help you understand the codebase, architecture, and get you up and running quickly.

---

## 1. Project Overview

### What is this system?

This is an **internal HR portal** that manages employees, leave requests, and payroll for an organization. It provides a complete REST API built with Python FastAPI and includes a single-page HTML frontend for easy interaction.

### Key Features

- **Employee Management**: Add, view, and manage employee records
- **Leave Management**: Apply for leave, track balances, approve/reject requests
- **Payroll Processing**: Calculate salaries, taxes, deductions, and generate payslips
- **Real-time Dashboard**: Interactive web interface for all HR operations

### Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | FastAPI (Python 3.x) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Data Storage** | In-memory (Python dictionaries) |
| **Testing** | pytest |
| **API Documentation** | FastAPI auto-generated (Swagger/OpenAPI) |
| **Server** | Uvicorn (ASGI server) |

### Target Users

- HR administrators managing employee records
- Managers approving leave requests
- Employees viewing their payroll and leave information

---

## 2. Architecture — How Files Connect

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Browser                              │
│                  (static/index.html)                         │
│              HTML + CSS + JavaScript                         │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/JSON
                     │ (Fetch API)
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Application                             │
│                  (app/main.py)                               │
│  • Routes & Endpoints                                        │
│  • Request Validation (Pydantic)                             │
│  • CORS Middleware                                           │
│  • Static File Serving                                       │
└──────┬──────────────┬──────────────┬────────────────────────┘
       │              │              │
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  employee.py│ │   leave.py  │ │  payroll.py │
│             │ │             │ │             │
│ • CRUD ops  │ │ • Apply     │ │ • Calculate │
│ • Validation│ │ • Approve   │ │ • Tax       │
│ • Experience│ │ • Balance   │ │ • Payslip   │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │              │              │
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ employees{} │ │leave_records│ │payroll_     │
│             │ │leave_balances│ │history{}    │
│ In-Memory   │ │ In-Memory   │ │ In-Memory   │
└─────────────┘ └─────────────┘ └─────────────┘
```

### Module Dependencies

```
app/main.py
    ├── imports app.employee
    ├── imports app.leave
    └── imports app.payroll
        └── imports app.employee (for get_employee)
```

### Data Flow Example: Leave Application

```
1. User clicks "Apply Leave" in browser
2. JavaScript sends POST to /leave/apply
3. main.py receives request, validates with Pydantic
4. main.py calls employee.get_employee() to verify employee exists
5. main.py calls leave.apply_leave() with validated data
6. leave.py checks eligibility and creates leave record
7. leave.py returns leave record dict
8. main.py returns JSON response to browser
9. JavaScript updates UI with success message
```

### In-Memory Storage Architecture

**Critical Understanding**: All data lives in Python dictionaries at module level.

- **Advantages**: Fast, simple, no database setup
- **Limitations**: Data resets on server restart, not production-ready

**Storage Locations**:
- `app/employee.py`: `employees = {emp_id: {...}}`
- `app/leave.py`: `leave_records = {leave_id: {...}}`, `leave_balances = {emp_id: {...}}`
- `app/payroll.py`: `payroll_history = {emp_id: [...]}`

---

## 3. File-by-File Explanation

### 📄 `app/main.py` (127 lines)

**Purpose**: FastAPI application entry point, API routing, and request handling.

**What it does**:
- Defines the FastAPI application instance
- Configures CORS middleware for cross-origin requests
- Mounts static files directory for serving frontend
- Defines Pydantic models for request validation
- Implements 9 API endpoints
- Handles errors and converts them to HTTP responses

**Key Components**:

```python
# FastAPI app instance
app = FastAPI(title="HR Employee Management System")

# Pydantic models for validation
class EmployeeCreate(BaseModel):
    name: str
    department: str
    salary: float
    manager: Optional[int] = None

# Example endpoint
@app.post("/employees", status_code=201)
def create_employee(data: EmployeeCreate):
    return employee.add_employee(data.name, data.department, data.salary, data.manager)
```

**Endpoints Defined**:
1. `GET /health` - Health check
2. `GET /employees` - List all employees
3. `POST /employees` - Add new employee
4. `GET /employees/{emp_id}` - Get employee by ID
5. `GET /leave/{emp_id}` - Get leave balance and history
6. `POST /leave/apply` - Apply for leave
7. `POST /leave/approve` - Approve leave
8. `GET /payroll/{emp_id}` - Get payroll details
9. `GET /payroll/{emp_id}/payslip` - Generate payslip

**Error Handling Pattern**:
```python
try:
    result = business_logic_function()
    return result
except ValueError as e:
    raise HTTPException(status_code=400/404, detail=str(e))
```

---

### 📄 `app/employee.py` (92 lines)

**Purpose**: Employee data management and business logic.

**What it does**:
- Stores employee records in `employees` dictionary
- Provides CRUD operations for employees
- Calculates employee experience
- Filters employees by department

**Data Structure**:
```python
employees = {
    1: {
        "id": 1,
        "name": "Raj Kumar",
        "department": "Engineering",
        "join_date": "2020-03-15",
        "salary": 75000,
        "manager": None
    }
}
```

**Functions** (6 total):
1. `add_employee()` - Create new employee with auto-ID
2. `get_employee()` - Retrieve by ID (raises ValueError if not found)
3. `list_employees()` - Return all employees
4. `update_salary()` - Update salary with validation
5. `calculate_experience_years()` - Calculate years since join_date
6. `get_employees_by_department()` - Filter by department (case-insensitive)

**Sample Data**: 5 pre-seeded employees (IDs 1-5)

**Key Logic**:
- Auto-incrementing ID using `_next_id` global variable
- Join date automatically set to today on creation
- Experience calculated using: `(today - join_date).days // 365`

---

### 📄 `app/leave.py` (89 lines)

**Purpose**: Leave management system with application, approval, and balance tracking.

**What it does**:
- Manages leave applications and their lifecycle
- Tracks leave balances per employee
- Validates leave eligibility
- Handles approval/rejection workflow

**Leave Types**:
```python
LEAVE_TYPES = {
    "annual": 18,      # days per year
    "sick": 10,
    "maternity": 182,
    "paternity": 5
}
```

**Data Structures**:
```python
# Leave applications
leave_records = {
    1: {
        "leave_id": 1,
        "emp_id": 1,
        "leave_type": "annual",
        "days": 3,
        "status": "pending",  # pending/approved/rejected
        "applied_on": "2026-05-01",
        "approved_by": None,
        "rejection_reason": None
    }
}

# Employee balances
leave_balances = {
    1: {"annual": 18, "sick": 10, "maternity": 182, "paternity": 5}
}
```

**Functions** (6 total):
1. `apply_leave()` - Create leave application (status: pending)
2. `approve_leave()` - Approve and deduct from balance
3. `reject_leave()` - Reject without deducting balance
4. `get_leave_balance()` - Get current balances (initializes if needed)
5. `check_leave_eligibility()` - Check if balance > 0
6. `get_leave_history()` - Get all leave records for employee

**Workflow**:
```
Apply (pending) → Approve (deduct balance) OR Reject (no deduction)
```

**Important**: Balance is deducted only on approval, not on application.

---

### 📄 `app/payroll.py` (69 lines)

**Purpose**: Payroll calculations including salary, tax, deductions, and payslip generation.

**What it does**:
- Calculates monthly salary from annual
- Applies Indian income tax slabs
- Handles deductions (tax, PF)
- Generates and stores payslips
- Calculates bonuses

**Data Structure**:
```python
payroll_history = {
    1: [  # emp_id
        {
            "emp_id": 1,
            "month": 5,
            "year": 2026,
            "gross_salary": 6250.0,
            "deductions": {"tax": 0.0, "pf": 750.0},
            "net_salary": 5500.0
        }
    ]
}
```

**Functions** (6 total):
1. `calculate_monthly_salary()` - Annual / 12
2. `calculate_tax()` - Apply Indian tax slabs
3. `apply_deductions()` - Subtract deductions from salary
4. `generate_payslip()` - Create payslip for month/year
5. `get_payroll_history()` - Get all payslips for employee
6. `calculate_bonus()` - Calculate bonus percentage

**Tax Calculation**:
- Annualizes monthly salary (× 12)
- Applies progressive tax slabs
- Divides annual tax by 12 for monthly deduction

**PF Deduction**: 12% of monthly gross salary

---

### 📄 `static/index.html` (362 lines)

**Purpose**: Single-page frontend application for HR operations.

**What it does**:
- Provides tabbed interface (Employees, Leave, Payroll)
- Makes API calls using Fetch API
- Displays data in tables and cards
- Handles form submissions
- Shows success/error messages

**Architecture**:
- Pure HTML/CSS/JavaScript (no frameworks)
- Inline styles for simplicity
- Event-driven JavaScript functions

**Key JavaScript Functions**:
- `loadEmployees()` - Fetch and display employee list
- `addEmployee()` - POST new employee
- `loadLeave()` - Fetch leave balance and history
- `applyLeave()` - POST leave application
- `approveLeave()` - POST leave approval
- `loadPayroll()` - Fetch payroll details
- `generatePayslip()` - Generate payslip

**UI Features**:
- Responsive design
- Loading spinners
- Success/error messages (auto-dismiss after 4 seconds)
- Formatted currency display (₹)
- Status badges (pending/approved/rejected)

---

### 📄 `tests/test_employee.py` (147 lines)

**Purpose**: Unit tests for employee module.

**Test Classes** (6):
1. `TestAddEmployee` - Test employee creation
2. `TestGetEmployee` - Test retrieval by ID
3. `TestListEmployees` - Test listing all employees
4. `TestUpdateSalary` - Test salary updates
5. `TestCalculateExperienceYears` - Test experience calculation
6. `TestGetEmployeesByDepartment` - Test department filtering

**Test Pattern**:
```python
class TestFunctionName:
    def setup_method(self):
        _reset()  # Reset data before each test
    
    def test_specific_scenario(self):
        # Arrange, Act, Assert
```

**Coverage**: CRUD operations, validation, edge cases, error handling

---

### 📄 `tests/test_leave.py` (166 lines)

**Purpose**: Unit tests for leave management.

**Test Classes** (6):
1. `TestGetLeaveBalance` - Test balance retrieval
2. `TestCheckLeaveEligibility` - Test eligibility checks
3. `TestApplyLeave` - Test leave application
4. `TestApproveLeave` - Test approval workflow
5. `TestRejectLeave` - Test rejection workflow
6. `TestGetLeaveHistory` - Test history retrieval

**Key Tests**:
- Balance initialization
- Application validation
- Approval deducts balance
- Rejection doesn't deduct balance
- Status transitions

---

### 📄 `tests/test_payroll.py` (188 lines)

**Purpose**: Unit tests for payroll calculations.

**Test Classes** (6):
1. `TestCalculateMonthlySalary` - Test salary calculation
2. `TestApplyDeductions` - Test deduction logic
3. `TestCalculateTax` - Test tax slab application
4. `TestGeneratePayslip` - Test payslip generation
5. `TestGetPayrollHistory` - Test history retrieval
6. `TestCalculateBonus` - Test bonus calculation

**Key Tests**:
- Tax slab boundaries
- Deduction calculations
- Payslip idempotency
- Negative value handling

---

## 4. Key Functions Reference

### Employee Module Functions

#### `add_employee(name: str, department: str, salary: float, manager: Optional[int] = None) -> dict`

Creates a new employee with auto-generated ID and today's join date.

**Example**:
```python
emp = add_employee("Kavya Nair", "Engineering", 75000, manager=1)
# Returns: {"id": 6, "name": "Kavya Nair", "department": "Engineering", 
#           "join_date": "2026-05-01", "salary": 75000, "manager": 1}
```

#### `get_employee(emp_id: int) -> dict`

Retrieves employee by ID. Raises `ValueError` if not found.

**Example**:
```python
emp = get_employee(1)
# Returns: {"id": 1, "name": "Raj Kumar", ...}
```

#### `list_employees() -> list`

Returns all employees as a list.

#### `update_salary(emp_id: int, new_salary: float) -> dict`

Updates employee salary. Validates salary >= 0.

#### `calculate_experience_years(emp_id: int) -> int`

Calculates full years since join date using `(today - join_date).days // 365`.

#### `get_employees_by_department(department: str) -> list`

Filters employees by department (case-insensitive).

---

### Leave Module Functions

#### `apply_leave(emp_id: int, leave_type: str, days: int, reason: str) -> dict`

Creates leave application with status "pending". Validates type and eligibility.

**Example**:
```python
leave = apply_leave(1, "annual", 3, "Family vacation")
# Returns: {"leave_id": 1, "emp_id": 1, "status": "pending", ...}
```

#### `approve_leave(leave_id: int, approved_by: int) -> dict`

Approves pending leave and deducts from balance.

**Example**:
```python
approved = approve_leave(1, approved_by=2)
# Returns: {"leave_id": 1, "status": "approved", "approved_by": 2, ...}
```

#### `reject_leave(leave_id: int, reason: str) -> dict`

Rejects pending leave. Does NOT deduct balance.

#### `get_leave_balance(emp_id: int) -> dict`

Returns current balance for all leave types. Initializes defaults on first call.

**Example**:
```python
balance = get_leave_balance(1)
# Returns: {"emp_id": 1, "balances": {"annual": 18, "sick": 10, ...}}
```

#### `check_leave_eligibility(emp_id: int, leave_type: str) -> bool`

Returns True if employee has balance > 0 for the leave type.

#### `get_leave_history(emp_id: int) -> list`

Returns all leave records for employee (all statuses).

---

### Payroll Module Functions

#### `calculate_monthly_salary(emp_id: int) -> float`

Calculates monthly gross: `annual_salary / 12`, rounded to 2 decimals.

**Example**:
```python
monthly = calculate_monthly_salary(1)  # Annual: 75000
# Returns: 6250.0
```

#### `calculate_tax(salary: float) -> float`

Applies Indian tax slabs to monthly salary.

**Tax Slabs** (Annual):
- Up to ₹2,50,000: 0%
- ₹2,50,001 – ₹5,00,000: 5% on amount above ₹2,50,000
- ₹5,00,001 – ₹10,00,000: ₹12,500 + 20% on amount above ₹5,00,000
- Above ₹10,00,000: ₹1,12,500 + 30% on amount above ₹10,00,000

**Example**:
```python
tax = calculate_tax(6250.0)  # Annual: 75000 < 250000
# Returns: 0.0
```

#### `apply_deductions(salary: float, deductions: dict) -> float`

Subtracts deductions from salary. Floors at 0.

**Example**:
```python
net = apply_deductions(6250.0, {"tax": 0, "pf": 750})
# Returns: 5500.0
```

#### `generate_payslip(emp_id: int, month: int, year: int) -> dict`

Generates payslip with gross, deductions, and net salary. Stores in history (idempotent).

**Example**:
```python
payslip = generate_payslip(1, 5, 2026)
# Returns: {"emp_id": 1, "month": 5, "year": 2026, 
#           "gross_salary": 6250.0, "net_salary": 5500.0, ...}
```

#### `get_payroll_history(emp_id: int) -> list`

Returns all generated payslips for employee.

#### `calculate_bonus(emp_id: int, percentage: float) -> float`

Calculates bonus: `annual_salary * (percentage / 100)`.

---

## 5. How to Run Locally

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Terminal/Command Prompt
- Web browser

### Setup Steps

#### 1. Clone Repository

```bash
git clone https://github.com/sworna-vidhya-m/hr-code-onboarding-bob.git
cd hr-code-onboarding-bob
```

#### 2. Create Virtual Environment

**macOS/Linux**:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**:
```bash
python -m venv .venv
.venv\Scripts\activate
```

You should see `(.venv)` in your terminal prompt.

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Installs: FastAPI, Uvicorn, Pydantic, pytest, and other dependencies.

#### 4. Start Development Server

```bash
uvicorn app.main:app --reload
```

**Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

**Flags**:
- `--reload`: Auto-restart on code changes (development only)
- `--host 0.0.0.0`: Make accessible from network
- `--port 8080`: Use different port

#### 5. Access Application

- **Frontend**: http://localhost:8000/
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

#### 6. Run Tests

In a new terminal (keep server running):

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_employee.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

#### 7. Stop Server

Press `CTRL+C` in the terminal running uvicorn.

#### 8. Deactivate Virtual Environment

```bash
deactivate
```

### Troubleshooting

**Port in use**:
```bash
uvicorn app.main:app --reload --port 8080
```

**Module not found**:
```bash
pip install -r requirements.txt
```

**Tests failing**:
```bash
pytest --cache-clear
pytest tests/ -vv
```

---

## 6. Business Rules Summary

### Tax Calculation (Indian Income Tax Slabs)

| Annual Income | Tax Rate | Calculation |
|---------------|----------|-------------|
| Up to ₹2,50,000 | 0% | No tax |
| ₹2,50,001 – ₹5,00,000 | 5% | 5% on amount above ₹2,50,000 |
| ₹5,00,001 – ₹10,00,000 | 20% | ₹12,500 + 20% on amount above ₹5,00,000 |
| Above ₹10,00,000 | 30% | ₹1,12,500 + 30% on amount above ₹10,00,000 |

**Process**:
1. Monthly salary is annualized (× 12)
2. Tax calculated on annual income
3. Annual tax divided by 12 for monthly deduction
4. Rounded to 2 decimal places

**Examples**:

```
Employee: ₹75,000 annual
Annual: 75,000 < 2,50,000
Tax: 0
Monthly Tax: 0

Employee: ₹6,00,000 annual
Annual: 6,00,000
Tax: 12,500 + (6,00,000 - 5,00,000) × 0.20 = 32,500
Monthly Tax: 32,500 / 12 = 2,708.33

Employee: ₹15,00,000 annual
Annual: 15,00,000
Tax: 1,12,500 + (15,00,000 - 10,00,000) × 0.30 = 2,62,500
Monthly Tax: 2,62,500 / 12 = 21,875.00
```

### Provident Fund (PF) Deduction

- **Rate**: 12% of monthly gross salary
- **Applied to**: All employees
- **Calculation**: `monthly_gross × 0.12`
- **Example**: Monthly gross ₹6,250 → PF ₹750

### Leave Entitlements

| Leave Type | Days/Year | Purpose |
|------------|-----------|---------|
| Annual | 18 | Vacation, personal time |
| Sick | 10 | Illness, medical |
| Maternity | 182 | Maternity (6 months) |
| Paternity | 5 | Paternity |

### Leave Workflow Rules

**Application**:
- Must specify valid leave type
- Days must be > 0
- System checks eligibility (balance > 0)
- Status set to "pending"
- Balance NOT deducted yet

**Approval**:
- Only "pending" leaves can be approved
- System re-checks balance
- Balance deducted upon approval
- Approver ID recorded

**Rejection**:
- Only "pending" leaves can be rejected
- Balance NOT deducted
- Rejection reason recorded

**Balance Management**:
- Initialized to default entitlements on first access
- Tracked per employee per leave type
- Deducted only on approval

### Salary Rules

- Cannot be negative
- Changes take effect immediately
- Affects future payroll calculations
- No retroactive changes to past payslips

### Employee Rules

- ID auto-incremented (starts at 6)
- Join date set to today on creation
- Manager field optional (not validated)
- Department is case-sensitive in storage

### Data Persistence

⚠️ **Critical**: All data is in-memory

- Server restart resets to sample data
- 5 pre-seeded employees (IDs 1-5)
- No leave records or payroll history on startup
- Not suitable for production without database

---

## 7. First Steps for New Developer

### Quick Start Checklist

- [ ] Clone repository
- [ ] Set up virtual environment
- [ ] Install dependencies
- [ ] Start server
- [ ] Explore frontend at http://localhost:8000
- [ ] Check API docs at http://localhost:8000/docs
- [ ] Run tests
- [ ] Read this guide

### Day 1: Explore the System

**1. Use the Frontend** (30 min)
- Add an employee
- Apply for leave
- Generate a payslip
- Watch API calls in browser DevTools (Network tab)

**2. Read the Code** (2 hours)
- Start with `app/main.py` - understand endpoints
- Read `app/employee.py` - see data management
- Read `app/leave.py` - understand workflow
- Read `app/payroll.py` - see calculations

**3. Run Tests** (1 hour)
- Run `pytest tests/ -v`
- Read test files
- Modify a test and see it fail

### Day 2: Make Your First Change

**Suggested Task**: Add "Get Employee by Name" endpoint

```python
# 1. Add function in app/employee.py
def get_employee_by_name(name: str) -> Optional[dict]:
    for emp in employees.values():
        if emp["name"].lower() == name.lower():
            return emp
    return None

# 2. Add endpoint in app/main.py
@app.get("/employees/search/{name}")
def search_employee(name: str):
    emp = employee.get_employee_by_name(name)
    if emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

# 3. Add test in tests/test_employee.py
def test_get_employee_by_name():
    emp = get_employee_by_name("Raj Kumar")
    assert emp["id"] == 1
```

### Common Development Tasks

**Adding New Endpoint**:
1. Add business logic in appropriate module
2. Add Pydantic model (if needed) in main.py
3. Add endpoint in main.py
4. Add tests
5. Update frontend (if needed)

**Debugging Tips**:
- Use print statements
- Check server logs (uvicorn output)
- Use API docs to test endpoints
- Use browser DevTools
- Run tests in isolation

### Your First Week Goals

- [ ] Explain system architecture
- [ ] Add a new API endpoint with tests
- [ ] Understand leave approval workflow
- [ ] Explain tax calculation
- [ ] Debug a failing test
- [ ] Make a frontend change

### Known Limitations

1. No data persistence (resets on restart)
2. No authentication/authorization
3. No audit trail
4. Manager IDs not validated
5. No pagination
6. No search/filtering
7. No email notifications

**Good First Projects**:
- Add database integration
- Add user authentication
- Add role-based permissions
- Add email notifications
- Add search functionality
- Add pagination
- Add audit logging

---

## Conclusion

You now have a comprehensive understanding of the HR Employee Management System. Start by exploring the frontend, reading the code, and running tests. Make small changes to build confidence, and refer back to this guide as needed.

**Key Takeaways**:
- FastAPI backend with 3 core modules
- In-memory storage (not production-ready)
- Leave workflow: Apply → Pending → Approve/Reject
- Indian tax slabs with progressive rates
- Comprehensive test coverage with pytest

**Next Steps**:
1. Set up your development environment
2. Explore the running application
3. Read through the code files
4. Make your first code change
5. Add tests for your changes

Welcome to the team! 🚀
