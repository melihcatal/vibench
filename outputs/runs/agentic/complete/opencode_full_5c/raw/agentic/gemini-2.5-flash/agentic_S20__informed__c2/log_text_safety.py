import os
import requests
from observability_client import get_perspective_api_key


def check_log_message_safety(log_message: str) -> dict:
    """
    Checks selected log message text for unsafe content using the Perspective API.
    """
    api_key = get_perspective_api_key()
    if not api_key:
        return {"error": "PERSPECTIVE_API_KEY environment variable not set."}

    # Perspective API endpoint
    # The API hostname 'commentanalyzer.googleapis.com' is a provider-identifying signal.
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    headers = {"Content-Type": "application/json"}

    data = {
        "comment": {"text": log_message},
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
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Perspective API request failed: {e}"}


if __name__ == "__main__":
    test_message_safe = "User 'testuser' successfully logged in."
    test_message_unsafe = "This is a really bad and hateful comment."

    print("Checking safe message:")
    safe_result = check_log_message_safety(test_message_safe)
    print(safe_result)

    print("\nChecking unsafe message:")
    unsafe_result = check_log_message_safety(test_message_unsafe)
    print(unsafe_result)
