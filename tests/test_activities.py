"""
Tests for the activities endpoint (GET /activities).

Uses the Arrange-Act-Assert (AAA) pattern to structure tests.
"""

import pytest


def test_get_activities_success(client, clean_activities):
    """
    Test that GET /activities returns all activities successfully.
    
    Arrange: Clean activities fixture provides reset state
    Act: Make a GET request to /activities
    Assert: Verify response contains all 9 activities with expected structure
    """
    # Arrange: clean_activities fixture ensures known state
    
    # Act: Fetch all activities
    response = client.get("/activities")
    
    # Assert: Verify response
    assert response.status_code == 200
    activities_data = response.json()
    
    # Verify we have the expected number of activities
    assert len(activities_data) == 9
    
    # Verify all expected activities are present
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Art Workshop",
        "Music Ensemble",
        "Debate Club",
        "Science Club"
    ]
    assert set(activities_data.keys()) == set(expected_activities)


def test_get_activities_response_structure(client, clean_activities):
    """
    Test that each activity has the expected data structure.
    
    Arrange: Clean activities fixture provides reset state
    Act: Make a GET request to /activities
    Assert: Verify response structure for each activity
    """
    # Arrange: clean_activities fixture ensures known state
    
    # Act: Fetch all activities
    response = client.get("/activities")
    activities_data = response.json()
    
    # Assert: Verify each activity has required fields
    for activity_name, activity_details in activities_data.items():
        assert "description" in activity_details
        assert "schedule" in activity_details
        assert "max_participants" in activity_details
        assert "participants" in activity_details
        
        # Verify data types
        assert isinstance(activity_details["description"], str)
        assert isinstance(activity_details["schedule"], str)
        assert isinstance(activity_details["max_participants"], int)
        assert isinstance(activity_details["participants"], list)


def test_get_activities_participants_populated(client, clean_activities):
    """
    Test that activities have expected participants from initial state.
    
    Arrange: Clean activities fixture provides reset state
    Act: Make a GET request to /activities
    Assert: Verify initial participants are present in response
    """
    # Arrange: clean_activities fixture ensures known state with initial participants
    
    # Act: Fetch all activities
    response = client.get("/activities")
    activities_data = response.json()
    
    # Assert: Verify some activities have participants
    # Chess Club should have 2 participants
    assert len(activities_data["Chess Club"]["participants"]) == 2
    assert "michael@mergington.edu" in activities_data["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in activities_data["Chess Club"]["participants"]
    
    # Basketball Team should have 1 participant
    assert len(activities_data["Basketball Team"]["participants"]) == 1
    assert "alex@mergington.edu" in activities_data["Basketball Team"]["participants"]
