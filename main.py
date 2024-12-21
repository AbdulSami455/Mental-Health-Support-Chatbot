import streamlit as st
import logging
from api_llm import generate_response
from ui_helpers import chat_bubble
from user_management import list_users, save_user, get_user

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)

st.title("Mental Health Support Chatbot")

# Fetch the list of users and log any errors
try:
    users = list_users()
    logging.info("User list fetched successfully.")
except Exception as e:
    logging.error(f"Error fetching user list: {e}")
    users = []

# Initialize session state for user details and chat messages
if 'user_details' not in st.session_state:
    st.session_state['user_details'] = {}

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Sidebar: Select or create a user
st.sidebar.title("User Management")
selected_user = st.sidebar.selectbox("Existing Users", ["New User"] + users)

if selected_user == "New User":
    with st.sidebar.form(key='new_user_form'):
        name = st.text_input("Enter your name:")
        age = st.number_input("Enter your age:", min_value=0, max_value=120, step=1)
        gender = st.selectbox("Select your gender:", ["Male", "Female", "Other"])
        health_record = st.text_area("Any previous health record or concerns?")
        submit_user = st.form_submit_button(label='Create User')

        if submit_user:
            st.session_state['user_details'] = {
                'name': name,
                'age': age,
                'gender': gender,
                'health_record': health_record,
                'sleep_pattern': 'Average',
                'stress_level': 5,
                'support_system': 'Prefer not to say',
                'daily_routine': '',
                'ongoing_treatment': ''
            }
            try:
                save_user(st.session_state['user_details'])
                logging.info(f"User created: {st.session_state['user_details']}")
                st.success(f"User {name} created successfully.")
            except Exception as e:
                logging.error(f"Error creating user: {e}")
                st.error("Error creating user.")
else:
    # Load selected user
    try:
        user_data = get_user(selected_user)
        if user_data:
            st.session_state['user_details'] = user_data
            logging.info(f"Loaded user data: {user_data}")
        else:
            st.warning(f"No data found for user: {selected_user}")
    except Exception as e:
        logging.error(f"Error loading user data for {selected_user}: {e}")
        st.error("Error loading user data.")

# Chat interface
if 'user_details' in st.session_state and st.session_state['user_details']:
    user_details = st.session_state['user_details']
    st.markdown(f"### Chat with {user_details['name']}")

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for sender, message in st.session_state['messages']:
            st.markdown(chat_bubble(sender, message), unsafe_allow_html=True)

    # Input box and send button
    with st.form(key='chat_form', clear_on_submit=True):
        user_message = st.text_input("Type your message:")
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_message:
        logging.info(f"User message received: {user_message}")
        try:
            # Prepare detailed prompt
            detailed_prompt = (
                f"User Details:\n"
                f"Name: {user_details['name']}\n"
                f"Age: {user_details['age']}\n"
                f"Gender: {user_details['gender']}\n"
                f"Health Record: {user_details['health_record']}\n"
                f"Sleep Pattern: {user_details.get('sleep_pattern', 'Average')}\n"
                f"Stress Level: {user_details.get('stress_level', 5)}\n"
                f"Support System: {user_details.get('support_system', 'Prefer not to say')}\n"
                f"Daily Routine: {user_details.get('daily_routine', '')}\n"
                f"Ongoing Treatment: {user_details.get('ongoing_treatment', '')}\n\n"
                f"User Query: {user_message}"
            )
            logging.debug(f"Prompt sent to LLM: {detailed_prompt}")

            response = generate_response(detailed_prompt)
            if not response.strip():
                response = "I'm sorry, I couldn't process your request. Please try again."
                logging.warning("Received empty or invalid response from LLM.")

            logging.debug(f"Response received from LLM: {response}")
            st.session_state['messages'].append(("You", user_message))
            st.session_state['messages'].append(("Assistant", response))

            with chat_container:
                st.markdown(chat_bubble("You", user_message), unsafe_allow_html=True)
                st.markdown(chat_bubble("Assistant", response), unsafe_allow_html=True)

        except Exception as e:
            logging.error(f"Error during LLM interaction: {e}")
            st.error("An error occurred while processing your message. Please try again.")
