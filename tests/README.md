# FastAPI Tests Documentation

## Overview
Comprehensive test suite for the Mergington High School Activities API using pytest and FastAPI's TestClient.

## Test Structure

### Files Created
- `tests/conftest.py` - Pytest configuration and fixtures
- `tests/test_activities.py` - Main test suite for activity endpoints

### Dependencies Added to requirements.txt
- `pytest` - Testing framework
- `httpx` - Required by FastAPI's TestClient

## Test Coverage

### Test Classes

#### TestGetActivities (4 tests)
Tests for the GET `/activities` endpoint:
- `test_get_activities_returns_all_activities` - Verifies all 9 activities are returned
- `test_get_activities_contains_required_fields` - Ensures each activity has required fields (description, schedule, max_participants, participants)
- `test_get_activities_participants_is_list` - Validates participants field is a list
- `test_chess_club_has_initial_participants` - Verifies initial participants are present

#### TestSignupForActivity (6 tests)
Tests for the POST `/activities/{activity_name}/signup` endpoint:
- `test_signup_successful` - Successful signup returns expected message
- `test_signup_adds_participant` - Signup actually adds the participant to the activity
- `test_signup_activity_not_found` - Returns 404 when activity doesn't exist
- `test_signup_already_registered` - Prevents duplicate signups (400 error)
- `test_signup_multiple_students` - Multiple students can sign up for same activity
- `test_signup_same_student_different_activities` - Students can sign up for multiple activities

#### TestRootEndpoint (1 test)
Tests for the root endpoint:
- `test_root_redirects_to_static` - Verifies GET / redirects to /static/index.html

## Running Tests

```bash
# Run all tests
pytest tests/test_activities.py -v

# Run specific test class
pytest tests/test_activities.py::TestGetActivities -v

# Run specific test
pytest tests/test_activities.py::TestGetActivities::test_get_activities_returns_all_activities -v

# Run with coverage
pytest tests/test_activities.py --cov=src --cov-report=html
```

## Test Results
✅ All 11 tests passing successfully

## Fixtures

### client
Provides a TestClient instance for making HTTP requests to the FastAPI app.

### reset_activities
Resets the in-memory activities database to its initial state before each test and cleans up afterward. This ensures test isolation.

## Notes
- Tests use query parameters for signup (e.g., `?email=test@mergington.edu`)
- Activity names with spaces are URL-encoded (e.g., `Chess%20Club`)
- Tests validate both successful scenarios and error conditions
- The fixture prevents test pollution by resetting data between tests
