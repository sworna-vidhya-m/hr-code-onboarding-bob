from datetime import date, datetime
from typing import Optional

employees: dict = {
    1: {
        "id": 1,
        "name": "Raj Kumar",
        "department": "Engineering",
        "join_date": "2020-03-15",
        "salary": 75000,
        "manager": None,
    },
    2: {
        "id": 2,
        "name": "Priya Sharma",
        "department": "HR",
        "join_date": "2019-07-01",
        "salary": 65000,
        "manager": 1,
    },
    3: {
        "id": 3,
        "name": "Arun Patel",
        "department": "Finance",
        "join_date": "2021-01-10",
        "salary": 70000,
        "manager": 1,
    },
    4: {
        "id": 4,
        "name": "Meena Iyer",
        "department": "Engineering",
        "join_date": "2018-11-20",
        "salary": 80000,
        "manager": None,
    },
    5: {
        "id": 5,
        "name": "Suresh Babu",
        "department": "Operations",
        "join_date": "2022-06-05",
        "salary": 60000,
        "manager": 2,
    },
}

_next_id: int = 6


def add_employee(name: str, department: str, salary: float, manager: Optional[int] = None) -> dict:
    global _next_id
    emp = {
        "id": _next_id,
        "name": name,
        "department": department,
        "join_date": date.today().isoformat(),
        "salary": salary,
        "manager": manager,
    }
    employees[_next_id] = emp
    _next_id += 1
    return emp


def get_employee(emp_id: int) -> dict:
    if emp_id not in employees:
        raise ValueError(f"Employee {emp_id} not found")
    return employees[emp_id]


def list_employees() -> list:
    return list(employees.values())


def update_salary(emp_id: int, new_salary: float) -> dict:
    if emp_id not in employees:
        raise ValueError(f"Employee {emp_id} not found")
    if new_salary < 0:
        raise ValueError("Salary cannot be negative")
    employees[emp_id]["salary"] = new_salary
    return employees[emp_id]


def calculate_experience_years(emp_id: int) -> int:
    emp = get_employee(emp_id)
    join = datetime.strptime(emp["join_date"], "%Y-%m-%d").date()
    today = date.today()
    return (today - join).days // 365


def get_employees_by_department(department: str) -> list:
    return [e for e in employees.values() if e["department"].lower() == department.lower()]
