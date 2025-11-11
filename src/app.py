"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },

    # Sports-related activities
    "Basketball Team": {
        "description": "Competitive basketball practices and matches",
        "schedule": "Mondays, Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Casual play and intramural soccer matches",
        "schedule": "Tuesdays, Thursdays, 4:30 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["ava@mergington.edu", "isabella@mergington.edu"]
    },

    # Artistic activities
    "Art Club": {
        "description": "Drawing, painting, and mixed-media workshops",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["mia@mergington.edu", "charlotte@mergington.edu"]
    },
    "Photography Club": {
        "description": "Learn photography techniques and organize exhibitions",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },

    # Intellectual activities
    "Debate Team": {
        "description": "Practice public speaking and compete in debate tournaments",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["elijah@mergington.edu", "lucas@mergington.edu"]
    },
    "Math Club": {
        "description": "Problem solving, math contests preparation, and puzzles",
        "schedule": "Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["sophia2@mergington.edu", "jack@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
# Validate student is not already signed up

def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate student is not already signed up
    if email in activities[activity_name]["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
