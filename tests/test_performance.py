import pytest
from datetime import date
from app import performance


@pytest.fixture(autouse=True)
def reset_performance_data():
    """Reset performance data before each test."""
    performance.reviews.clear()
    performance._next_review_id = 1
    yield
    # Cleanup after test
    performance.reviews.clear()
    performance._next_review_id = 1


class TestAddReview:
    """Tests for add_review function."""
    
    def test_add_review_success(self):
        """Test adding a valid review."""
        review = performance.add_review(
            emp_id=1,
            rating=5,
            comments="Excellent work",
            reviewer_id=2
        )
        
        assert review["emp_id"] == 1
        assert review["rating"] == 5
        assert review["comments"] == "Excellent work"
        assert review["reviewer_id"] == 2
        assert "review_id" in review
        assert "review_date" in review
        assert review["review_date"] == date.today().isoformat()
    
    def test_add_review_invalid_rating_too_high(self):
        """Test adding review with rating > 5."""
        with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
            performance.add_review(1, 6, "Test", 2)
    
    def test_add_review_invalid_rating_too_low(self):
        """Test adding review with rating < 1."""
        with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
            performance.add_review(1, 0, "Test", 2)
    
    def test_add_review_invalid_rating_negative(self):
        """Test adding review with negative rating."""
        with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
            performance.add_review(1, -1, "Test", 2)
    
    def test_add_multiple_reviews_same_employee(self):
        """Test adding multiple reviews for the same employee."""
        review1 = performance.add_review(1, 4, "Good work", 2)
        review2 = performance.add_review(1, 5, "Excellent improvement", 2)
        
        assert review1["review_id"] != review2["review_id"]
        reviews = performance.get_reviews(1)
        assert len(reviews) >= 2
    
    def test_add_review_new_employee(self):
        """Test adding review for employee with no previous reviews."""
        review = performance.add_review(99, 3, "Average performance", 1)
        
        assert review["emp_id"] == 99
        assert 99 in performance.reviews
        assert len(performance.reviews[99]) == 1
    
    def test_add_review_increments_id(self):
        """Test that review IDs increment correctly."""
        initial_id = performance._next_review_id
        review1 = performance.add_review(1, 4, "Test 1", 2)
        review2 = performance.add_review(2, 5, "Test 2", 1)
        
        assert review2["review_id"] == review1["review_id"] + 1


class TestGetReviews:
    """Tests for get_reviews function."""
    
    def test_get_reviews_existing_employee(self):
        """Test getting reviews for employee with reviews."""
        reviews = performance.get_reviews(1)
        
        assert isinstance(reviews, list)
        assert len(reviews) > 0
        assert all(r["emp_id"] == 1 for r in reviews)
    
    def test_get_reviews_no_reviews(self):
        """Test getting reviews for employee with no reviews."""
        reviews = performance.get_reviews(999)
        
        assert isinstance(reviews, list)
        assert len(reviews) == 0
    
    def test_get_reviews_returns_all(self):
        """Test that get_reviews returns all reviews for an employee."""
        performance.add_review(10, 3, "Review 1", 1)
        performance.add_review(10, 4, "Review 2", 1)
        performance.add_review(10, 5, "Review 3", 1)
        
        reviews = performance.get_reviews(10)
        assert len(reviews) == 3


class TestGetLatestReview:
    """Tests for get_latest_review function."""
    
    def test_get_latest_review_existing(self):
        """Test getting latest review for employee with reviews."""
        latest = performance.get_latest_review(1)
        
        assert isinstance(latest, dict)
        assert "rating" in latest
        assert "comments" in latest
        assert latest["emp_id"] == 1
    
    def test_get_latest_review_no_reviews(self):
        """Test getting latest review for employee with no reviews."""
        latest = performance.get_latest_review(999)
        
        assert isinstance(latest, dict)
        assert len(latest) == 0
    
    def test_get_latest_review_returns_most_recent(self):
        """Test that get_latest_review returns the most recent review."""
        performance.add_review(20, 3, "Old review", 1)
        performance.add_review(20, 4, "Newer review", 1)
        latest_review = performance.add_review(20, 5, "Latest review", 1)
        
        latest = performance.get_latest_review(20)
        assert latest["review_id"] == latest_review["review_id"]
        assert latest["rating"] == 5
        assert latest["comments"] == "Latest review"


class TestCalculatePerformanceBonus:
    """Tests for calculate_performance_bonus function."""
    
    def test_bonus_rating_5(self):
        """Test bonus calculation for rating 5."""
        performance.add_review(30, 5, "Excellent", 1)
        bonus = performance.calculate_performance_bonus(30)
        assert bonus == 20.0
    
    def test_bonus_rating_4(self):
        """Test bonus calculation for rating 4."""
        performance.add_review(31, 4, "Good", 1)
        bonus = performance.calculate_performance_bonus(31)
        assert bonus == 15.0
    
    def test_bonus_rating_3(self):
        """Test bonus calculation for rating 3."""
        performance.add_review(32, 3, "Average", 1)
        bonus = performance.calculate_performance_bonus(32)
        assert bonus == 10.0
    
    def test_bonus_rating_2(self):
        """Test bonus calculation for rating 2."""
        performance.add_review(33, 2, "Needs improvement", 1)
        bonus = performance.calculate_performance_bonus(33)
        assert bonus == 5.0
    
    def test_bonus_rating_1(self):
        """Test bonus calculation for rating 1."""
        performance.add_review(34, 1, "Poor", 1)
        bonus = performance.calculate_performance_bonus(34)
        assert bonus == 0.0
    
    def test_bonus_no_reviews(self):
        """Test bonus calculation for employee with no reviews."""
        bonus = performance.calculate_performance_bonus(999)
        assert bonus == 0.0
    
    def test_bonus_uses_latest_review(self):
        """Test that bonus uses the latest review rating."""
        performance.add_review(40, 2, "Old review", 1)
        performance.add_review(40, 5, "Latest review", 1)
        
        bonus = performance.calculate_performance_bonus(40)
        assert bonus == 20.0


class TestGetPerformanceBadge:
    """Tests for get_performance_badge function."""
    
    def test_badge_rating_5(self):
        """Test badge for rating 5."""
        performance.add_review(50, 5, "Excellent", 1)
        badge = performance.get_performance_badge(50)
        assert badge == "Excellent"
    
    def test_badge_rating_4(self):
        """Test badge for rating 4."""
        performance.add_review(51, 4, "Good", 1)
        badge = performance.get_performance_badge(51)
        assert badge == "Good"
    
    def test_badge_rating_3(self):
        """Test badge for rating 3."""
        performance.add_review(52, 3, "Average", 1)
        badge = performance.get_performance_badge(52)
        assert badge == "Average"
    
    def test_badge_rating_2(self):
        """Test badge for rating 2."""
        performance.add_review(53, 2, "Needs improvement", 1)
        badge = performance.get_performance_badge(53)
        assert badge == "Needs Improvement"
    
    def test_badge_rating_1(self):
        """Test badge for rating 1."""
        performance.add_review(54, 1, "Poor", 1)
        badge = performance.get_performance_badge(54)
        assert badge == "Needs Improvement"
    
    def test_badge_no_reviews(self):
        """Test badge for employee with no reviews."""
        badge = performance.get_performance_badge(999)
        assert badge == "No Review"
    
    def test_badge_uses_latest_review(self):
        """Test that badge uses the latest review rating."""
        performance.add_review(60, 2, "Old review", 1)
        performance.add_review(60, 5, "Latest review", 1)
        
        badge = performance.get_performance_badge(60)
        assert badge == "Excellent"


class TestGetTeamPerformance:
    """Tests for get_team_performance function."""
    
    def test_team_performance_engineering(self):
        """Test getting team performance for Engineering department."""
        team_perf = performance.get_team_performance("Engineering")
        
        assert isinstance(team_perf, list)
        assert len(team_perf) > 0
        assert all(emp["department"] == "Engineering" for emp in team_perf)
    
    def test_team_performance_hr(self):
        """Test getting team performance for HR department."""
        team_perf = performance.get_team_performance("HR")
        
        assert isinstance(team_perf, list)
        assert len(team_perf) > 0
        assert all(emp["department"] == "HR" for emp in team_perf)
    
    def test_team_performance_includes_all_fields(self):
        """Test that team performance includes all required fields."""
        team_perf = performance.get_team_performance("Engineering")
        
        for emp in team_perf:
            assert "emp_id" in emp
            assert "name" in emp
            assert "department" in emp
            assert "rating" in emp
            assert "badge" in emp
            assert "bonus_percentage" in emp
            assert "review_date" in emp
    
    def test_team_performance_empty_department(self):
        """Test getting team performance for non-existent department."""
        team_perf = performance.get_team_performance("NonExistent")
        
        assert isinstance(team_perf, list)
        assert len(team_perf) == 0
    
    def test_team_performance_case_insensitive(self):
        """Test that department lookup is case-insensitive."""
        team_perf_lower = performance.get_team_performance("engineering")
        team_perf_upper = performance.get_team_performance("ENGINEERING")
        
        assert len(team_perf_lower) == len(team_perf_upper)
    
    def test_team_performance_with_no_reviews(self):
        """Test team performance includes employees without reviews."""
        # Add a new employee without reviews
        from app.employee import add_employee
        new_emp = add_employee("Test Employee", "Engineering", 70000, None)
        
        team_perf = performance.get_team_performance("Engineering")
        
        # Find the new employee in results
        new_emp_perf = next((e for e in team_perf if e["emp_id"] == new_emp["id"]), None)
        assert new_emp_perf is not None
        assert new_emp_perf["rating"] == 0
        assert new_emp_perf["badge"] == "No Review"
        assert new_emp_perf["bonus_percentage"] == 0.0


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_rating_boundary_1(self):
        """Test rating at lower boundary (1)."""
        review = performance.add_review(70, 1, "Minimum rating", 1)
        assert review["rating"] == 1
    
    def test_rating_boundary_5(self):
        """Test rating at upper boundary (5)."""
        review = performance.add_review(71, 5, "Maximum rating", 1)
        assert review["rating"] == 5
    
    def test_empty_comments(self):
        """Test adding review with empty comments."""
        review = performance.add_review(72, 3, "", 1)
        assert review["comments"] == ""
    
    def test_very_long_comments(self):
        """Test adding review with very long comments."""
        long_comment = "A" * 1000
        review = performance.add_review(73, 4, long_comment, 1)
        assert review["comments"] == long_comment
    
    def test_same_employee_reviewer(self):
        """Test adding review where employee and reviewer are the same."""
        review = performance.add_review(74, 3, "Self review", 74)
        assert review["emp_id"] == 74
        assert review["reviewer_id"] == 74
    
    def test_multiple_employees_same_reviewer(self):
        """Test one reviewer reviewing multiple employees."""
        review1 = performance.add_review(80, 4, "Review 1", 1)
        review2 = performance.add_review(81, 5, "Review 2", 1)
        review3 = performance.add_review(82, 3, "Review 3", 1)
        
        assert review1["reviewer_id"] == 1
        assert review2["reviewer_id"] == 1
        assert review3["reviewer_id"] == 1

# Made with Bob
