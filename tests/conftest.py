"""
Pytest configuration and fixtures for FastAPI tests.

This module provides shared fixtures for all tests using the Arrange-Act-Assert pattern.
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path so we can import the app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """
    Fixture providing a TestClient instance for the FastAPI app.
    
    Arrange: Initialize a fresh TestClient with the app instance
    """
    return TestClient(app)


@pytest.fixture
def clean_activities():
    """
    Fixture that resets activities to initial state before each test.
    
    Arrange: Reset the activities database to a known clean state
    """
    # Store original activities
    original_activities = {
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
        "Basketball Team": {
            "description": "Competitive basketball practice and games",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and compete in matches",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["sarah@mergington.edu", "james@mergington.edu"]
        },
        "Art Workshop": {
            "description": "Explore painting, drawing, and mixed media techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["maya@mergington.edu"]
        },
        "Music Ensemble": {
            "description": "Join our orchestra and perform classical and modern pieces",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["lucas@mergington.edu", "isabella@mergington.edu"]
        },
        "Debate Club": {
            "description": "Develop critical thinking and public speaking skills",
            "schedule": "Mondays, 3:30 PM - 4:30 PM",
            "max_participants": 16,
            "participants": ["ryan@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific discoveries",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["lucy@mergington.edu", "noah@mergington.edu"]
        }
    }
    
    # Clear current activities and restore originals
    activities.clear()
    activities.update(original_activities)
    
    yield activities
    
    # Cleanup: Reset activities after test completes
    activities.clear()
    activities.update(original_activities)
