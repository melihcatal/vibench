import os
import requests
import json

# Perspective API endpoint (publicly available for testing/development)
PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_message_safety(text_payload: str) -> dict:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{PERSPECTIVE_API_ENDPOINT}?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text_payload},
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

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

if __name__ == "__main__":
    # Example usage:
    # Set PERSPECTIVE_API_KEY environment variable (obtain from Google Cloud Console)
    # from your terminal: export PERSPECTIVE_API_KEY="your-perspective-api-key"

    unsafe_text = "You are an idiot!"
    safe_text = "This is a polite message."

    print("Checking unsafe text:")
    result_unsafe = check_message_safety(unsafe_text)
    print(json.dumps(result_unsafe, indent=2))

    print("
Checking safe text:")
    result_safe = check_message_safety(safe_text)
    print(json.dumps(result_safe, indent=2))
