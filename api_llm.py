import requests
import logging

# Configure logging for API calls
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("api.log"),
        logging.StreamHandler()
    ]
)

OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "cniongolo/biomistral:latest"
CONTENT = (
    "You are a compassionate and empathetic Mental Health Assistant. Your role is to provide thoughtful, "
    "supportive, and non-judgmental guidance to users seeking help with their mental health. Be understanding, "
    "kind, and ensure your responses are evidence-based and practical. Do not provide medical diagnoses or treatments, "
    "but encourage users to seek professional help if needed. Keep your tone positive and uplifting while addressing "
    "their concerns with care and clarity."
)

def generate_response(prompt):
    """Send a request to the API and return the assistant's response."""
    logging.info("Generating response from LLM...")
    logging.debug(f"Prompt: {prompt}")

    try:
        response = requests.post(
            OLLAMA_API_URL,
            headers={"Content-Type": "application/json"},
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": CONTENT},
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }
        )

        if response.status_code == 200:
            data = response.json()
            logging.debug(f"Raw API response: {data}")

            # Extract and validate the response content
            content = data.get("message", {}).get("content", "").strip()
            if not content:
                logging.warning("Response content is empty or missing.")
                return "I'm sorry, I couldn't provide an answer. Please try again or rephrase your question."

            return content
        else:
            logging.error(f"API responded with error: {response.status_code} - {response.text}")
            return f"Error: {response.status_code} - Unable to process your query at this time."
    except Exception as e:
        logging.exception("An error occurred while communicating with the LLM API.")
        return "An unexpected error occurred while processing your query. Please try again later."
