"""Automated tests for the chatbot application."""

import pytest

# Import the Flask app and helper functions
from app import app, check_for_crisis


from app import sanitise_input


class TestChatAPI:
    """Tests for the /chat API endpoint."""

    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app."""
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_empty_message_rejected(self, client):
        """TC-002: Empty messages should return an error."""
        response = client.post("/chat", json={"message": ""})
        data = response.get_json()
        assert "Please enter a message" in data["response"]

    def test_long_message_rejected(self, client):
        """TC-003: Messages over 500 chars should return an error."""
        long_message = "a" * 501
        response = client.post("/chat", json={"message": long_message})
        data = response.get_json()
        assert "too long" in data["response"].lower()

    def test_normal_message_gets_response(self, client):
        """TC-001: Normal messages should get a bot response."""
        response = client.post("/chat", json={"message": "Hello"})
        data = response.get_json()
        assert "response" in data
        assert len(data["response"]) > 0
