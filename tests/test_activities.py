"""Tests for FastAPI activities endpoints."""

import pytest


class TestGetActivities:
    """Tests for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Test that GET /activities returns all activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        assert len(data) == 9

    def test_get_activities_contains_required_fields(self, client, reset_activities):
        """Test that each activity has required fields."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data

    def test_get_activities_participants_is_list(self, client, reset_activities):
        """Test that participants field is a list."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list)

    def test_chess_club_has_initial_participants(self, client, reset_activities):
        """Test that Chess Club has initial participants."""
        response = client.get("/activities")
        data = response.json()
        
        assert len(data["Chess Club"]["participants"]) == 2
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in data["Chess Club"]["participants"]


class TestSignupForActivity:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_successful(self, client, reset_activities):
        """Test successful signup for an activity."""
        response = client.post(
            "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Signed up" in data["message"]
        assert "newstudent@mergington.edu" in data["message"]

    def test_signup_adds_participant(self, client, reset_activities):
        """Test that signup actually adds the participant to the activity."""
        # Sign up
        response = client.post(
            "/activities/Programming%20Class/signup?email=test@mergington.edu"
        )
        assert response.status_code == 200
        
        # Verify participant was added
        response = client.get("/activities")
        data = response.json()
        assert "test@mergington.edu" in data["Programming Class"]["participants"]

    def test_signup_activity_not_found(self, client, reset_activities):
        """Test signup fails when activity doesn't exist."""
        response = client.post(
            "/activities/NonExistentActivity/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_already_registered(self, client, reset_activities):
        """Test that a student cannot sign up twice for the same activity."""
        # Try to sign up with an email already registered
        response = client.post(
            "/activities/Chess%20Club/signup?email=michael@mergington.edu"
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_multiple_students(self, client, reset_activities):
        """Test that multiple students can sign up for the same activity."""
        # First student signs up
        response1 = client.post(
            "/activities/Art%20Club/signup?email=student1@mergington.edu"
        )
        assert response1.status_code == 200
        
        # Second student signs up
        response2 = client.post(
            "/activities/Art%20Club/signup?email=student2@mergington.edu"
        )
        assert response2.status_code == 200
        
        # Verify both were added
        response = client.get("/activities")
        data = response.json()
        assert "student1@mergington.edu" in data["Art Club"]["participants"]
        assert "student2@mergington.edu" in data["Art Club"]["participants"]

    def test_signup_same_student_different_activities(self, client, reset_activities):
        """Test that a student can sign up for multiple different activities."""
        # Sign up for Chess Club
        response1 = client.post(
            "/activities/Chess%20Club/signup?email=versatile@mergington.edu"
        )
        assert response1.status_code == 200
        
        # Sign up for Programming Class
        response2 = client.post(
            "/activities/Programming%20Class/signup?email=versatile@mergington.edu"
        )
        assert response2.status_code == 200
        
        # Verify student is in both
        response = client.get("/activities")
        data = response.json()
        assert "versatile@mergington.edu" in data["Chess Club"]["participants"]
        assert "versatile@mergington.edu" in data["Programming Class"]["participants"]


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_redirects_to_static(self, client):
        """Test that GET / redirects to /static/index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert "/static/index.html" in response.headers.get("location", "")
