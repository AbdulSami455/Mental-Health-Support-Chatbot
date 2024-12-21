import streamlit as st
import unittest
from unittest.mock import patch, MagicMock
from ..main import generate_response, list_users, save_user, get_user

class TestMain(unittest.TestCase):

    @patch("main.generate_response")
    def test_generate_response(self, mock_generate_response):
        mock_generate_response.return_value = "Test response"
        response = generate_response("Test prompt")
        self.assertEqual(response, "Test response")

    @patch("main.list_users")
    def test_list_users(self, mock_list_users):
        mock_list_users.return_value = ["Alice", "Bob"]
        users = list_users()
        self.assertIn("Alice", users)
        self.assertIn("Bob", users)

    @patch("main.save_user")
    def test_save_user(self, mock_save_user):
        user_data = {"name": "Test User", "age": 30}
        save_user(user_data)
        mock_save_user.assert_called_once_with(user_data)

    @patch("main.get_user")
    def test_get_user(self, mock_get_user):
        mock_get_user.return_value = {"name": "Test User", "age": 30}
        user = get_user("Test User")
        self.assertEqual(user["name"], "Test User")
        self.assertEqual(user["age"], 30)

if __name__ == "__main__":
    unittest.main()