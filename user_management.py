import json
import bcrypt

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

def save_users(users):
    """Save all users to the JSON file."""
    try:
        with open(USERS_FILE, "w") as file:
            json.dump(users, file, indent=4)
    except Exception as e:
        print(f"Error saving users: {e}")

def list_users():
    """Return a list of all registered usernames."""
    users = load_users()
    return list(users.keys())

def register_user(user_profile):
    """Register a new user with all profile details."""
    users = load_users()
    username = user_profile["username"]
    if username in users:
        raise ValueError("Username already exists.")
    hashed_password = bcrypt.hashpw(user_profile["password"].encode(), bcrypt.gensalt()).decode()
    user_profile["password"] = hashed_password
    users[username] = user_profile
    save_users(users)

def authenticate_user(username, password):
    """Authenticate a user by verifying their password."""
    users = load_users()
    if username not in users:
        return False
    stored_password = users[username]["password"].encode()
    return bcrypt.checkpw(password.encode(), stored_password)
