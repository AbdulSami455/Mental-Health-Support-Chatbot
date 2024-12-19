import json

USERS_FILE = "users.json"

def load_users():
    """Load all users from the JSON file."""
    try:
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Error loading users: {e}")
        return {}

def save_user(user_details):
    """Save user details to the JSON file."""
    users = load_users()
    users[user_details['name']] = user_details
    try:
        with open(USERS_FILE, "w") as file:
            json.dump(users, file, indent=4)
    except Exception as e:
        print(f"Error saving user: {e}")

def get_user(name):
    """Retrieve a specific user's data by name."""
    users = load_users()
    return users.get(name, None)

def list_users():
    """Return a list of all user names."""
    users = load_users()
    return list(users.keys())
