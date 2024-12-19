import requests

OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "cniongolo/biomistral:latest"
CONTENT = "You are a compassionate and empathetic Mental Health Assistant. Your role is to provide thoughtful, supportive, and non-judgmental guidance to users seeking help with their mental health. Be understanding, kind, and ensure your responses are evidence-based and practical. Do not provide medical diagnoses or treatments, but encourage users to seek professional help if needed. Keep your tone positive and uplifting while addressing their concerns with care and clarity."


def generate_response(prompt):
    """Send a request to the API and return the assistant's response."""
    

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
            return data["message"].get("content", "Error: No content found.").strip()
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"
    