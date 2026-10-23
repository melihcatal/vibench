import os
import requests
from typing import Dict, Any

def check_log_text_safety(log_message: str, client_ip: str = None) -> Dict[str, Any]:
    """Checks selected log message text for unsafe content using the Perspective API."""
    # Ensure PERSPECTIVE_API_KEY environment variable is set
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        return {"error": "PERSPECTIVE_API_KEY environment variable not set."}

    # Perspective API endpoint
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    request_body = {
        "comment": {"text": log_message},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"]
    }

    if client_ip:
        request_body["doNotStore"] = True # Privacy consideration for user data
        request_body["sessionId"] = client_ip # Use IP as a session ID for logging purposes

    try:
        response = requests.post(url, json=request_body)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error calling Perspective API: {e}"}

if __name__ == "__main__":
    # Example usage:
    # Ensure PERSPECTIVE_API_KEY environment variable is set
    sample_log_message_safe = "User 'testuser' logged in successfully from 192.168.1.1."
    sample_log_message_unsafe = "Bad user activity detected: Go to hell!"

    print("\nChecking safe message:")
    result_safe = check_log_text_safety(sample_log_message_safe)
    print(result_safe)

    print("\nChecking unsafe message:")
    result_unsafe = check_log_text_safety(sample_log_message_unsafe, client_ip="192.168.1.100")
    print(result_unsafe)
