from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from datetime import date
import os

from app import employee, leave, payroll, performance

app = FastAPI(title="HR Employee Management System")

# Initialize sample performance data after all modules are loaded
performance._initialize_sample_data()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


class EmployeeCreate(BaseModel):
    name: str
    department: str
    salary: float
    manager: Optional[int] = None


class LeaveApply(BaseModel):
    emp_id: int
    leave_type: str
    days: int
    reason: str


class LeaveApprove(BaseModel):
    leave_id: int
    approved_by: int


@app.get("/health")
def health():
    return {"status": "ok", "service": "HR Employee Management System"}


@app.get("/employees")
def list_employees():
    return employee.list_employees()


@app.post("/employees", status_code=201)
def create_employee(data: EmployeeCreate):
    return employee.add_employee(data.name, data.department, data.salary, data.manager)


@app.get("/employees/{emp_id}")
def get_employee(emp_id: int):
    try:
        return employee.get_employee(emp_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/leave/{emp_id}")
def leave_balance(emp_id: int):
    try:
        employee.get_employee(emp_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    balance = leave.get_leave_balance(emp_id)
    history = leave.get_leave_history(emp_id)
    return {**balance, "history": history}


@app.post("/leave/apply")
def apply_leave(data: LeaveApply):
    try:
        employee.get_employee(data.emp_id)
        return leave.apply_leave(data.emp_id, data.leave_type, data.days, data.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/leave/approve")
def approve_leave(data: LeaveApprove):
    try:
        return leave.approve_leave(data.leave_id, data.approved_by)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/payroll/{emp_id}")
def payroll_info(emp_id: int):
    try:
        emp = employee.get_employee(emp_id)
        gross = payroll.calculate_monthly_salary(emp_id)
        tax = payroll.calculate_tax(gross)
        pf = round(gross * 0.12, 2)
        net = payroll.apply_deductions(gross, {"tax": tax, "pf": pf})
        return {
            "emp_id": emp_id,
            "name": emp["name"],
            "annual_salary": emp["salary"],
            "monthly_gross": gross,
            "monthly_tax": tax,
            "monthly_pf": pf,
            "monthly_net": net,
            "experience_years": employee.calculate_experience_years(emp_id),
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/payroll/{emp_id}/payslip")
def get_payslip(emp_id: int, month: int = date.today().month, year: int = date.today().year):
    try:
        return payroll.generate_payslip(emp_id, month, year)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

class PerformanceReview(BaseModel):
    emp_id: int
    rating: int
    comments: str
    reviewer_id: int


@app.get("/performance/{emp_id}")
def get_performance(emp_id: int):
    try:
        employee.get_employee(emp_id)
        reviews_list = performance.get_reviews(emp_id)
        latest = performance.get_latest_review(emp_id)
        badge = performance.get_performance_badge(emp_id)
        bonus = performance.calculate_performance_bonus(emp_id)
        return {
            "emp_id": emp_id,
            "reviews": reviews_list,
            "latest_review": latest,
            "badge": badge,
            "bonus_percentage": bonus,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/performance/review", status_code=201)
def add_performance_review(data: PerformanceReview):
    try:
        employee.get_employee(data.emp_id)
        employee.get_employee(data.reviewer_id)
        return performance.add_review(data.emp_id, data.rating, data.comments, data.reviewer_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/performance/{emp_id}/badge")
def get_badge(emp_id: int):
    try:
        employee.get_employee(emp_id)
        badge = performance.get_performance_badge(emp_id)
        return {"emp_id": emp_id, "badge": badge}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/performance/{emp_id}/bonus")
def get_bonus(emp_id: int):
    try:
        emp = employee.get_employee(emp_id)
        bonus_percentage = performance.calculate_performance_bonus(emp_id)
        annual_salary = emp["salary"]
        bonus_amount = round(annual_salary * (bonus_percentage / 100), 2)
        return {
            "emp_id": emp_id,
            "bonus_percentage": bonus_percentage,
            "annual_salary": annual_salary,
            "bonus_amount": bonus_amount,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/performance/team/{dept}")
def get_team_performance(dept: str):
    team_perf = performance.get_team_performance(dept)
    return {"department": dept, "team_performance": team_perf}



@app.get("/")
def index():
    return FileResponse(os.path.join(static_dir, "index.html"))
