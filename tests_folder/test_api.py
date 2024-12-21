import unittest
from unittest.mock import patch
from ..api_llm import generate_response

class TestAPI(unittest.TestCase):

    @patch("api.requests.post")
    def test_generate_response_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"message": {"content": "Hello"}}

        response = generate_response("Hi")
        self.assertEqual(response, "Hello")

    @patch("api.requests.post")
    def test_generate_response_failure(self, mock_post):
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = "Internal Server Error"

        response = generate_response("Hi")
        self.assertIn("Error", response)

if __name__ == "__main__":
    unittest.main()