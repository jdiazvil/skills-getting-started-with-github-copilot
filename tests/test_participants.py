"""
Tests for the participant removal endpoint (DELETE /activities/{activity_name}/participants/{email}).

Uses the Arrange-Act-Assert (AAA) pattern to structure tests.
"""

import pytest


def test_remove_participant_successful(client, clean_activities):
    """
    Test successful removal of a participant from an activity (happy path).
    
    Arrange: Clean activities fixture provides reset state; select participant from Debate Club
    Act: DELETE request to remove the participant
    Assert: Verify response indicates success and participant is removed
    """
    # Arrange: clean_activities fixture ensures known state
    # Ryan is registered for Debate Club
    activity_name = "Debate Club"
    email_to_remove = "ryan@mergington.edu"
    
    # Verify the email is currently registered
    response_before = client.get("/activities")
    assert email_to_remove in response_before.json()[activity_name]["participants"]
    participants_before = len(response_before.json()[activity_name]["participants"])
    
    # Act: Remove the participant
    response = client.delete(
        f"/activities/{activity_name}/participants/{email_to_remove}"
    )
    
    # Assert: Verify response
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email_to_remove in result["message"]
    assert activity_name in result["message"]
    
    # Verify participant was removed
    response_after = client.get("/activities")
    participants_after = len(response_after.json()[activity_name]["participants"])
    assert participants_after == participants_before - 1
    assert email_to_remove not in response_after.json()[activity_name]["participants"]


def test_remove_participant_activity_not_found(client, clean_activities):
    """
    Test removing a participant from a non-existent activity (error case).
    
    Arrange: Clean activities fixture provides reset state; use invalid activity name
    Act: DELETE from a non-existent activity
    Assert: Verify 404 error is returned
    """
    # Arrange: clean_activities fixture ensures known state
    invalid_activity = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act: Try to remove from non-existent activity
    response = client.delete(
        f"/activities/{invalid_activity}/participants/{email}"
    )
    
    # Assert: Verify 404 error
    assert response.status_code == 404
    result = response.json()
    assert result["detail"] == "Activity not found"


def test_remove_participant_not_registered(client, clean_activities):
    """
    Test removing a participant who is not registered (error case).
    
    Arrange: Clean activities fixture provides reset state; use email not registered for activity
    Act: DELETE with email that's not in the participants list
    Assert: Verify 400 error is returned
    """
    # Arrange: clean_activities fixture ensures known state
    activity_name = "Art Workshop"
    unregistered_email = "notregistered@mergington.edu"
    
    # Verify the email is NOT currently registered
    response_check = client.get("/activities")
    assert unregistered_email not in response_check.json()[activity_name]["participants"]
    
    # Act: Try to remove someone not registered
    response = client.delete(
        f"/activities/{activity_name}/participants/{unregistered_email}"
    )
    
    # Assert: Verify 400 error
    assert response.status_code == 400
    result = response.json()
    assert result["detail"] == "Student is not signed up for this activity"


def test_remove_one_of_multiple_participants(client, clean_activities):
    """
    Test removing one participant when activity has multiple (data integrity check).
    
    Arrange: Clean activities fixture provides reset state; Chess Club has 2 participants
    Act: DELETE one of the two participants
    Assert: Verify only the specified participant is removed, other remains
    """
    # Arrange: clean_activities fixture ensures known state
    # Chess Club has michael@mergington.edu and daniel@mergington.edu
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"
    email_to_keep = "daniel@mergington.edu"
    
    # Verify both are registered
    response_check = client.get("/activities")
    participants_before = response_check.json()[activity_name]["participants"]
    assert email_to_remove in participants_before
    assert email_to_keep in participants_before
    assert len(participants_before) == 2
    
    # Act: Remove michael
    response = client.delete(
        f"/activities/{activity_name}/participants/{email_to_remove}"
    )
    
    # Assert: Verify only michael was removed
    assert response.status_code == 200
    
    response_check = client.get("/activities")
    participants_after = response_check.json()[activity_name]["participants"]
    assert email_to_remove not in participants_after
    assert email_to_keep in participants_after
    assert len(participants_after) == 1


def test_remove_participant_with_special_characters_in_email(client, clean_activities):
    """
    Test removing a participant with special characters in their email address.
    
    Arrange: Clean activities fixture provides reset state; signup a student with special chars
    Act: Sign them up, then delete them using proper URL encoding
    Assert: Verify successful removal
    """
    # Arrange: clean_activities fixture ensures known state
    activity_name = "Music Ensemble"
    special_email = "first+last@mergington.edu"
    
    # First, sign up this student
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": special_email}
    )
    assert signup_response.status_code == 200
    
    # Verify they're registered
    response_check = client.get("/activities")
    assert special_email in response_check.json()[activity_name]["participants"]
    
    # Act: Remove the participant with special email
    response = client.delete(
        f"/activities/{activity_name}/participants/{special_email}"
    )
    
    # Assert: Verify successful removal
    assert response.status_code == 200
    
    response_check = client.get("/activities")
    assert special_email not in response_check.json()[activity_name]["participants"]
