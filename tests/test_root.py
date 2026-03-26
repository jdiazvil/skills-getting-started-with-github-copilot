"""
Tests for the root endpoint (GET /).

Uses the Arrange-Act-Assert (AAA) pattern to structure tests.
"""

import pytest


def test_root_redirect(client):
    """
    Test that GET / redirects to /static/index.html.
    
    Arrange: TestClient is ready (provided by fixture)
    Act: Make a GET request to the root endpoint
    Assert: Verify the response is a redirect to /static/index.html
    """
    # Arrange: No additional setup needed
    
    # Act: Make the request
    response = client.get("/", follow_redirects=False)
    
    # Assert: Verify redirect status and location header
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_follows_to_static(client):
    """
    Test that following the redirect from GET / leads to the static index.html.
    
    Arrange: TestClient is ready (provided by fixture)
    Act: Make a GET request to root with redirect following enabled
    Assert: Verify the final response is the HTML content
    """
    # Arrange: No additional setup needed
    
    # Act: Make the request and follow redirects
    response = client.get("/", follow_redirects=True)
    
    # Assert: Verify successful response
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
