import unittest
import os
import json
from ..user_management import load_users, save_user, get_user, list_users

class TestUserManagement(unittest.TestCase):

    def setUp(self):
        self.users_file = "test_users.json"
        if os.path.exists(self.users_file):
            os.remove(self.users_file)
        self.test_data = {
            "Alice": {"name": "Alice", "age": 25},
            "Bob": {"name": "Bob", "age": 30}
        }
        with open(self.users_file, "w") as file:
            json.dump(self.test_data, file)

    def tearDown(self):
        if os.path.exists(self.users_file):
            os.remove(self.users_file)

    def test_load_users(self):
        users = load_users()
        self.assertIn("Alice", users)
        self.assertIn("Bob", users)

    def test_save_user(self):
        new_user = {"name": "Charlie", "age": 35}
        save_user(new_user)

        users = load_users()
        self.assertIn("Charlie", users)
        self.assertEqual(users["Charlie"], new_user)

    def test_get_user(self):
        user = get_user("Alice")
        self.assertEqual(user["name"], "Alice")

    def test_list_users(self):
        users = list_users()
        self.assertIn("Alice", users)
        self.assertIn("Bob", users)

if __name__ == "__main__":
    unittest.main()