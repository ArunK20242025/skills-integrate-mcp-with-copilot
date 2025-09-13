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
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        "category": "Club",
        "day": "Friday",
        "time": "15:30"
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        "category": "Class",
        "day": "Tuesday,Thursday",
        "time": "15:30"
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
        "category": "Sports",
        "day": "Monday,Wednesday,Friday",
        "time": "14:00"
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"],
        "category": "Sports",
        "day": "Tuesday,Thursday",
        "time": "16:00"
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"],
        "category": "Sports",
        "day": "Wednesday,Friday",
        "time": "15:30"
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"],
        "category": "Club",
        "day": "Thursday",
        "time": "15:30"
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"],
        "category": "Club",
        "day": "Monday,Wednesday",
        "time": "16:00"
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"],
        "category": "Club",
        "day": "Tuesday",
        "time": "15:30"
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"],
        "category": "Club",
        "day": "Friday",
        "time": "16:00"
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


from typing import Optional
from fastapi import Query

@app.get("/activities")
def get_activities(
    category: Optional[str] = None,
    day: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = Query(None, enum=["name", "time"]),
    sort_order: Optional[str] = Query("asc", enum=["asc", "desc"])
):
    # Start with all activities
    filtered_activities = dict(activities)

    # Apply category filter
    if category:
        filtered_activities = {
            name: activity for name, activity in filtered_activities.items()
            if activity["category"].lower() == category.lower()
        }

    # Apply day filter
    if day:
        filtered_activities = {
            name: activity for name, activity in filtered_activities.items()
            if day.lower() in activity["day"].lower()
        }

    # Apply search filter
    if search:
        search_lower = search.lower()
        filtered_activities = {
            name: activity for name, activity in filtered_activities.items()
            if search_lower in name.lower() or search_lower in activity["description"].lower()
        }

    # Convert to list for sorting
    activities_list = [{"name": name, **activity} for name, activity in filtered_activities.items()]

    # Apply sorting
    if sort_by == "name":
        activities_list.sort(key=lambda x: x["name"], reverse=(sort_order == "desc"))
    elif sort_by == "time":
        activities_list.sort(key=lambda x: x["time"], reverse=(sort_order == "desc"))

    return activities_list


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
