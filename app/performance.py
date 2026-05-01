from datetime import date
from typing import Optional

# In-memory storage for performance reviews
reviews: dict = {}
_next_review_id: int = 1


def add_review(emp_id: int, rating: int, comments: str, reviewer_id: int) -> dict:
    """Add a performance review for an employee.
    
    Args:
        emp_id: Employee ID
        rating: Performance rating (1-5)
        comments: Review comments
        reviewer_id: ID of the reviewer
        
    Returns:
        dict: The created review
        
    Raises:
        ValueError: If rating is not between 1 and 5
    """
    global _next_review_id
    
    if not 1 <= rating <= 5:
        raise ValueError("Rating must be between 1 and 5")
    
    review = {
        "review_id": _next_review_id,
        "emp_id": emp_id,
        "rating": rating,
        "comments": comments,
        "reviewer_id": reviewer_id,
        "review_date": date.today().isoformat(),
    }
    
    if emp_id not in reviews:
        reviews[emp_id] = []
    
    reviews[emp_id].append(review)
    _next_review_id += 1
    
    return review


def get_reviews(emp_id: int) -> list:
    """Get all performance reviews for an employee.
    
    Args:
        emp_id: Employee ID
        
    Returns:
        list: List of all reviews for the employee
    """
    return reviews.get(emp_id, [])


def get_latest_review(emp_id: int) -> dict:
    """Get the most recent performance review for an employee.
    
    Args:
        emp_id: Employee ID
        
    Returns:
        dict: The latest review or empty dict if no reviews exist
    """
    emp_reviews = reviews.get(emp_id, [])
    if not emp_reviews:
        return {}
    
    return emp_reviews[-1]


def calculate_performance_bonus(emp_id: int) -> float:
    """Calculate performance bonus percentage based on latest rating.
    
    Bonus structure:
    - Rating 5: 20%
    - Rating 4: 15%
    - Rating 3: 10%
    - Rating 2: 5%
    - Rating 1: 0%
    
    Args:
        emp_id: Employee ID
        
    Returns:
        float: Bonus percentage (0.0 to 20.0)
    """
    latest = get_latest_review(emp_id)
    if not latest:
        return 0.0
    
    rating = latest.get("rating", 0)
    bonus_map = {
        5: 20.0,
        4: 15.0,
        3: 10.0,
        2: 5.0,
        1: 0.0,
    }
    
    return bonus_map.get(rating, 0.0)


def get_performance_badge(emp_id: int) -> str:
    """Get performance badge based on latest rating.
    
    Badge structure:
    - Rating 5: Excellent
    - Rating 4: Good
    - Rating 3: Average
    - Rating 1-2: Needs Improvement
    
    Args:
        emp_id: Employee ID
        
    Returns:
        str: Performance badge
    """
    latest = get_latest_review(emp_id)
    if not latest:
        return "No Review"
    
    rating = latest.get("rating", 0)
    
    if rating == 5:
        return "Excellent"
    elif rating == 4:
        return "Good"
    elif rating == 3:
        return "Average"
    elif rating in [1, 2]:
        return "Needs Improvement"
    else:
        return "No Review"


def get_team_performance(department: str) -> list:
    """Get performance summary for all employees in a department.
    
    Args:
        department: Department name
        
    Returns:
        list: List of performance summaries for employees in the department
    """
    from app.employee import get_employees_by_department
    
    dept_employees = get_employees_by_department(department)
    team_performance = []
    
    for emp in dept_employees:
        emp_id = emp["id"]
        latest = get_latest_review(emp_id)
        
        performance = {
            "emp_id": emp_id,
            "name": emp["name"],
            "department": emp["department"],
            "rating": latest.get("rating", 0) if latest else 0,
            "badge": get_performance_badge(emp_id),
            "bonus_percentage": calculate_performance_bonus(emp_id),
            "review_date": latest.get("review_date", "N/A") if latest else "N/A",
        }
        team_performance.append(performance)
    
    return team_performance


# Initialize with sample reviews for all 5 existing employees
def _initialize_sample_data():
    """Initialize sample performance reviews for existing employees."""
    sample_reviews = [
        # Employee 1: Raj Kumar - Engineering
        {"emp_id": 1, "rating": 5, "comments": "Outstanding performance. Consistently delivers high-quality work and mentors junior team members.", "reviewer_id": 4},
        
        # Employee 2: Priya Sharma - HR
        {"emp_id": 2, "rating": 4, "comments": "Excellent work in employee engagement initiatives. Strong communication skills.", "reviewer_id": 1},
        
        # Employee 3: Arun Patel - Finance
        {"emp_id": 3, "rating": 4, "comments": "Very good analytical skills. Improved financial reporting processes significantly.", "reviewer_id": 1},
        
        # Employee 4: Meena Iyer - Engineering
        {"emp_id": 4, "rating": 5, "comments": "Exceptional technical leadership. Led multiple successful projects this year.", "reviewer_id": 1},
        
        # Employee 5: Suresh Babu - Operations
        {"emp_id": 5, "rating": 3, "comments": "Meets expectations. Good team player but needs to improve time management.", "reviewer_id": 2},
    ]
    
    for review in sample_reviews:
        add_review(
            emp_id=review["emp_id"],
            rating=review["rating"],
            comments=review["comments"],
            reviewer_id=review["reviewer_id"]
        )


# Initialize sample data when module is imported
# _initialize_sample_data()  # Moved to main.py to avoid circular import

# Made with Bob
