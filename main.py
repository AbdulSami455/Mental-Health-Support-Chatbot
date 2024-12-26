import streamlit as st
import logging
import json
from user_management import list_users, register_user, authenticate_user
from api_llm import generate_response
from ui_helpers import chat_bubble

USERS_CHAT_HISTORY_FILE = "user_chat_history.json"

# Logging setup
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)

def log_message(sender, message):
    """Log chat messages to the log file."""
    logging.info(f"{sender}: {message}")

def load_chat_history(username):
    """Load chat history for a specific user."""
    try:
        with open(USERS_CHAT_HISTORY_FILE, "r") as file:
            all_histories = json.load(file)
        return all_histories.get(username, [])
    except FileNotFoundError:
        return []
    except Exception as e:
        logging.error(f"Error loading chat history: {e}")
        return []

def save_chat_history(username, messages):
    """Save chat history for a specific user."""
    try:
        try:
            with open(USERS_CHAT_HISTORY_FILE, "r") as file:
                all_histories = json.load(file)
        except FileNotFoundError:
            all_histories = {}

        all_histories[username] = messages

        with open(USERS_CHAT_HISTORY_FILE, "w") as file:
            json.dump(all_histories, file, indent=4)
    except Exception as e:
        logging.error(f"Error saving chat history: {e}")

st.title(" Mental Health Support Chatbot")

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "user_details" not in st.session_state:
    st.session_state["user_details"] = {}
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if not st.session_state["authenticated"]:
    st.sidebar.title("Login or Register")
    action = st.sidebar.radio("Select Action", ["Login", "Register"])

    if action == "Login":
        with st.sidebar.form(key="login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")

        if login_button:
            if authenticate_user(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["messages"] = load_chat_history(username)
                logging.info(f"User logged in: {username}")
                st.success(f"Welcome back, {username}!")
            else:
                logging.warning(f"Failed login attempt for username: {username}")
                st.error("Invalid username or password.")

    elif action == "Register":
        with st.sidebar.form(key="register_form"):
            st.header("Create a New User")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            name = st.text_input("Full Name:")
            age = st.number_input("Age:", min_value=0, max_value=120, step=1)
            gender = st.selectbox("Gender:", ["Male", "Female", "Other"])
            health_record = st.text_area("Health Record (e.g., past concerns, medical history):")
            sleep_pattern = st.selectbox("Sleep Pattern:", ["Poor", "Average", "Good"])
            stress_level = st.slider("Stress Level (1-10):", min_value=1, max_value=10, value=5)
            support_system = st.selectbox("Support System:", ["Family", "Friends", "None", "Prefer not to say"])
            daily_routine = st.text_area("Describe your daily routine:")
            ongoing_treatment = st.text_area("Are you undergoing any treatment or therapy?")
            register_button = st.form_submit_button("Register")

        if register_button:
            if password != confirm_password:
                st.error("Passwords do not match.")
            else:
                try:
                    user_profile = {
                        "username": username,
                        "password": password,
                        "name": name,
                        "age": age,
                        "gender": gender,
                        "health_record": health_record,
                        "sleep_pattern": sleep_pattern,
                        "stress_level": stress_level,
                        "support_system": support_system,
                        "daily_routine": daily_routine,
                        "ongoing_treatment": ongoing_treatment,
                    }
                    register_user(user_profile)
                    logging.info(f"New user registered: {username}")
                    st.success("Registration successful. You can now log in.")
                except ValueError as e:
                    logging.error(f"Registration error: {e}")
                    st.error(str(e))
                except Exception as e:
                    logging.error(f"Unexpected error during registration: {e}")
                    st.error("An error occurred during registration. Please try again.")
else:
    st.sidebar.write(f"Logged in as: {st.session_state['username']}")
    logout = st.sidebar.button("Logout")
    if logout:
        save_chat_history(st.session_state["username"], st.session_state["messages"])
        logging.info(f"User logged out: {st.session_state['username']}")
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.session_state["messages"] = []
        st.experimental_rerun()

# Chat functionality
if st.session_state["authenticated"]:
    st.markdown(f"### Chat with the Mental Health Support Assistant")

    # Display chat history with styled bubbles
    chat_container = st.container()
    with chat_container:
        for sender, message in st.session_state["messages"]:
            st.markdown(chat_bubble(sender, message), unsafe_allow_html=True)

    # Input form for user message
    with st.form(key='chat_form', clear_on_submit=True):
        user_message = st.text_input("Type your message:")
        submit_button = st.form_submit_button("Send")

    # Handle user input and response
    if submit_button and user_message:
        log_message("You", user_message)
        user_profile = st.session_state.get("user_details", {})
        context = f"User Details: {user_profile}\nUser Query: {user_message}"
        response = generate_response(context)

        # Append user message and assistant response to chat history
        st.session_state["messages"].append(("You", user_message))
        st.session_state["messages"].append(("Assistant", response))

        # Log assistant response
        log_message("Assistant", response)

        # Save chat history
        save_chat_history(st.session_state["username"], st.session_state["messages"])

        # Re-render chat history
        with chat_container:
            st.markdown(chat_bubble("You", user_message), unsafe_allow_html=True)
            st.markdown(chat_bubble("Assistant", response), unsafe_allow_html=True)
