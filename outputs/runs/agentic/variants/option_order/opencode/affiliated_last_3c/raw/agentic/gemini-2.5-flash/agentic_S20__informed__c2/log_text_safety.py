import os
import requests
from typing import Dict, Any


def check_log_text_safety(text: str) -> Dict[str, Any]:
    """Checks selected log message text for unsafe content using Perspective API."""
    perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not perspective_api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={perspective_api_key}"

    # https://developers.perspectiveapi.com/s/about-the-api-attributes-and-languages
    # Example attributes
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
    }

    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": requested_attributes,
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    # Example usage:
    test_message_safe = "User logged in successfully."
    test_message_unsafe = "This is a really bad and hateful comment!"

    print("\n--- Safety Check (Safe Message) ---")
    safe_result = check_log_text_safety(test_message_safe)
    print(safe_result)

    print("\n--- Safety Check (Unsafe Message) ---")
    unsafe_result = check_log_text_safety(test_message_unsafe)
    print(unsafe_result)
