"""
Tests for the signup endpoint (POST /activities/{activity_name}/signup).

Uses the Arrange-Act-Assert (AAA) pattern to structure tests.
"""

import pytest


def test_signup_successful(client, clean_activities):
    """
    Test successful signup for an activity (happy path).
    
    Arrange: Clean activities fixture provides reset state; select Programming Class with 2 participants
    Act: POST a new student email to the signup endpoint
    Assert: Verify response indicates success and participant is added
    """
    # Arrange: clean_activities fixture ensures known state
    activity_name = "Programming Class"
    new_email = "newstudent@mergington.edu"
    
    # Verify activity exists and count before signup
    response_before = client.get("/activities")
    participants_before = len(response_before.json()[activity_name]["participants"])
    
    # Act: Sign up the new student
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    # Assert: Verify response
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert new_email in result["message"]
    assert activity_name in result["message"]
    
    # Verify participant was added
    response_after = client.get("/activities")
    participants_after = len(response_after.json()[activity_name]["participants"])
    assert participants_after == participants_before + 1
    assert new_email in response_after.json()[activity_name]["participants"]


def test_signup_activity_not_found(client, clean_activities):
    """
    Test signup for a non-existent activity (error case).
    
    Arrange: Clean activities fixture provides reset state; use invalid activity name
    Act: POST to signup with a non-existent activity name
    Assert: Verify 404 error is returned
    """
    # Arrange: clean_activities fixture ensures known state
    invalid_activity = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act: Try to sign up for non-existent activity
    response = client.post(
        f"/activities/{invalid_activity}/signup",
        params={"email": email}
    )
    
    # Assert: Verify 404 error
    assert response.status_code == 404
    result = response.json()
    assert result["detail"] == "Activity not found"


def test_signup_already_registered(client, clean_activities):
    """
    Test signup when student is already registered (error case).
    
    Arrange: Clean activities fixture provides reset state; use existing participant from Chess Club
    Act: POST to signup with an email already registered for that activity
    Assert: Verify 400 error is returned
    """
    # Arrange: clean_activities fixture ensures known state
    # Michael is already registered for Chess Club
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    
    # Verify the email is currently registered
    response_check = client.get("/activities")
    assert existing_email in response_check.json()[activity_name]["participants"]
    
    # Act: Try to sign up with already-registered email
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email}
    )
    
    # Assert: Verify 400 error
    assert response.status_code == 400
    result = response.json()
    assert result["detail"] == "Student already signed up"


def test_signup_multiple_students_same_activity(client, clean_activities):
    """
    Test that multiple different students can sign up for the same activity.
    
    Arrange: Clean activities fixture provides reset state
    Act: Sign up two different students for Tennis Club
    Assert: Verify both are added successfully
    """
    # Arrange: clean_activities fixture ensures known state
    activity_name = "Tennis Club"
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    # Act: Sign up first student
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email1}
    )
    
    # Act: Sign up second student
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email2}
    )
    
    # Assert: Both signups successful
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Verify both are now registered
    response_check = client.get("/activities")
    participants = response_check.json()[activity_name]["participants"]
    assert email1 in participants
    assert email2 in participants
