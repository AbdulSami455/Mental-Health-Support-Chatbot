import streamlit as st
from api import generate_response
from ui_helpers import chat_bubble
from user_management import load_users, save_user, get_user, list_users

st.title("Mental Health Support Chatbot")

# List available users
users = list_users()

if 'user_details' not in st.session_state:
    st.session_state['user_details'] = {}

if not st.session_state['user_details']:
    st.sidebar.title("Select a User")
    selected_user = st.sidebar.selectbox("Existing Users", ["New User"] + users)

    if selected_user == "New User":
        # New user form
        with st.form(key='user_details_form'):
            name = st.text_input("Enter your name:")
            age = st.number_input("Enter your age:", min_value=0, max_value=120, step=1)
            gender = st.selectbox("Select your gender:", ["Male", "Female", "Other"])
            health_record = st.text_area("Any previous health record or concerns you'd like to share:")

            # Additional fields
            sleep_pattern = st.selectbox(
                "How would you describe your sleep pattern?",
                ["Very Good", "Good", "Average", "Poor", "Very Poor"]
            )
            stress_level = st.slider(
                "On a scale of 1 to 10, how stressed do you feel? (1 = Not stressed, 10 = Extremely stressed)",
                min_value=1, max_value=10
            )
            support_system = st.radio(
                "Do you have a support system (e.g., family, friends, therapist)?",
                ["Yes", "No", "Prefer not to say"]
            )
            daily_routine = st.text_area("Can you describe your typical daily routine?")
            ongoing_treatment = st.text_area("Are you undergoing any therapy or medication? If yes, please provide details.")

            submit_user_details = st.form_submit_button(label='Submit')

            if submit_user_details:
                st.session_state['user_details'] = {
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'health_record': health_record,
                    'sleep_pattern': sleep_pattern,
                    'stress_level': stress_level,
                    'support_system': support_system,
                    'daily_routine': daily_routine,
                    'ongoing_treatment': ongoing_treatment
                }
                save_user(st.session_state['user_details'])
                st.success("User details saved successfully.")
    else:
        # Load selected user
        user_data = get_user(selected_user)
        if user_data:
            st.session_state['user_details'] = user_data
            st.success(f"User data for {selected_user} loaded successfully.")

# Handle chat and book summaries
if 'user_details' in st.session_state and st.session_state['user_details'].get('name'):
    user_details = st.session_state['user_details']
    st.markdown(f"### Welcome, {user_details['name']}!")
    
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    with st.form(key='chat_form'):
        user_message = st.text_input("You:")
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_message:
        detailed_prompt = (
            f"User Details:\n"
            f"Name: {user_details['name']}\n"
            f"Age: {user_details['age']}\n"
            f"Gender: {user_details['gender']}\n"
            f"Health Record: {user_details['health_record']}\n"
            f"Sleep Pattern: {user_details['sleep_pattern']}\n"
            f"Stress Level: {user_details['stress_level']}\n"
            f"Support System: {user_details['support_system']}\n"
            f"Daily Routine: {user_details['daily_routine']}\n"
            f"Ongoing Treatment: {user_details['ongoing_treatment']}\n\n"
            f"User Query: {user_message}"
        )

        st.session_state['messages'].append(("You", user_message))
        response = generate_response(detailed_prompt)
        st.session_state['messages'].append(("Assistant", response))

    for sender, message in st.session_state['messages']:
        st.markdown(chat_bubble(sender, message), unsafe_allow_html=True)

famous_books = [
    "The Body Keeps the Score by Bessel van der Kolk",
    "Man's Search for Meaning by Viktor Frankl",
    "Feeling Good: The New Mood Therapy by David D. Burns",
    "The Happiness Trap by Russ Harris",
    "Lost Connections by Johann Hari",
]

def get_book_summary(book_name):
    prompt = f"Please provide a concise summary of the book: '{book_name}' and its importance to mental health. and summary must be 40-50 lines"
    return generate_response(prompt)

st.sidebar.title("Famous Mental Health Books")
for book in famous_books:
    if st.sidebar.button(book):
        summary = get_book_summary(book)
        st.markdown(f"### Summary for '{book}'")
        st.markdown(summary)

st.sidebar.title("Resources")
st.sidebar.write("If you need immediate help, please contact one of the following resources:")
st.sidebar.write("1. National Suicide Prevention Lifeline: 1-800-273-8255")
st.sidebar.write("2. Crisis Text Line: Text 'HELLO' to 741741")
st.sidebar.write("[More Resources](https://www.mentalhealth.gov/get-help/immediate-help)")
