import os
import requests

# Perspective API endpoint and key
# Ensure PERSPECTIVE_API_KEY environment variable is set
API_KEY = os.getenv("PERSPECTIVE_API_KEY")
API_BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_text_for_unsafe_content(text: str) -> dict:
    """Checks text for unsafe content using the Perspective API."""
    if not API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{API_BASE_URL}?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}
