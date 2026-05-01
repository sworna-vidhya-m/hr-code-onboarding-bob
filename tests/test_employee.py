import pytest
from app import employee as emp_module
from app.employee import (
    add_employee, get_employee, list_employees,
    update_salary, calculate_experience_years, get_employees_by_department,
)

SAMPLE = {
    1: {"id": 1, "name": "Raj Kumar", "department": "Engineering", "join_date": "2020-03-15", "salary": 75000, "manager": None},
    2: {"id": 2, "name": "Priya Sharma", "department": "HR", "join_date": "2019-07-01", "salary": 65000, "manager": 1},
    3: {"id": 3, "name": "Arun Patel", "department": "Finance", "join_date": "2021-01-10", "salary": 70000, "manager": 1},
    4: {"id": 4, "name": "Meena Iyer", "department": "Engineering", "join_date": "2018-11-20", "salary": 80000, "manager": None},
    5: {"id": 5, "name": "Suresh Babu", "department": "Operations", "join_date": "2022-06-05", "salary": 60000, "manager": 2},
}


def _reset():
    emp_module.employees.clear()
    emp_module.employees.update({k: dict(v) for k, v in SAMPLE.items()})
    emp_module._next_id = 6


class TestAddEmployee:
    def setup_method(self):
        _reset()

    def test_add_basic(self):
        e = add_employee("Test User", "IT", 50000)
        assert e["name"] == "Test User"
        assert e["department"] == "IT"
        assert e["salary"] == 50000
        assert e["id"] == 6

    def test_add_with_manager(self):
        e = add_employee("New Hire", "Engineering", 60000, manager=1)
        assert e["manager"] == 1

    def test_add_increments_id(self):
        e1 = add_employee("A", "HR", 40000)
        e2 = add_employee("B", "HR", 45000)
        assert e2["id"] == e1["id"] + 1

    def test_add_sets_join_date(self):
        e = add_employee("New", "Ops", 40000)
        assert e["join_date"] is not None
        assert len(e["join_date"]) == 10


class TestGetEmployee:
    def setup_method(self):
        _reset()

    def test_get_existing(self):
        e = get_employee(1)
        assert e["name"] == "Raj Kumar"

    def test_get_nonexistent(self):
        with pytest.raises(ValueError, match="not found"):
            get_employee(999)

    def test_get_returns_correct_data(self):
        e = get_employee(4)
        assert e["department"] == "Engineering"
        assert e["salary"] == 80000


class TestListEmployees:
    def setup_method(self):
        _reset()

    def test_list_returns_all(self):
        result = list_employees()
        assert len(result) == 5

    def test_list_is_list(self):
        assert isinstance(list_employees(), list)

    def test_list_after_add(self):
        add_employee("X", "IT", 50000)
        assert len(list_employees()) == 6


class TestUpdateSalary:
    def setup_method(self):
        _reset()

    def test_update_salary(self):
        e = update_salary(1, 90000)
        assert e["salary"] == 90000

    def test_update_persists(self):
        update_salary(2, 72000)
        assert get_employee(2)["salary"] == 72000

    def test_update_nonexistent(self):
        with pytest.raises(ValueError):
            update_salary(999, 50000)

    def test_negative_salary(self):
        with pytest.raises(ValueError, match="negative"):
            update_salary(1, -1000)


class TestCalculateExperienceYears:
    def setup_method(self):
        _reset()

    def test_experience_positive(self):
        years = calculate_experience_years(1)
        assert years >= 5

    def test_experience_more_senior(self):
        years_meena = calculate_experience_years(4)
        years_suresh = calculate_experience_years(5)
        assert years_meena > years_suresh

    def test_experience_nonexistent(self):
        with pytest.raises(ValueError):
            calculate_experience_years(999)

    def test_experience_returns_int(self):
        assert isinstance(calculate_experience_years(1), int)


class TestGetEmployeesByDepartment:
    def setup_method(self):
        _reset()

    def test_engineering_dept(self):
        result = get_employees_by_department("Engineering")
        assert len(result) == 2
        names = [e["name"] for e in result]
        assert "Raj Kumar" in names
        assert "Meena Iyer" in names

    def test_case_insensitive(self):
        result = get_employees_by_department("engineering")
        assert len(result) == 2

    def test_nonexistent_dept(self):
        result = get_employees_by_department("Nonexistent")
        assert result == []

    def test_single_dept(self):
        result = get_employees_by_department("HR")
        assert len(result) == 1
        assert result[0]["name"] == "Priya Sharma"
