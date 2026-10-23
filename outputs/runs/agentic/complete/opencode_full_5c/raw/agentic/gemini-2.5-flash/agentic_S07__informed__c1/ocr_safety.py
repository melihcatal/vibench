import requests
import os

PERSPECTIVE_API_BASE_URL = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def check_text_safety(text: str, api_key: str, do_not_store: bool = True):
    """Checks text for unsafe content using the Perspective API."""
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
        },
        "doNotStore": do_not_store,  # Set to True for production to avoid storing user data
    }
    headers = {"Content-Type": "application/json"}
    params = {"key": api_key}

    response = requests.post(
        PERSPECTIVE_API_BASE_URL, headers=headers, params=params, json=payload
    )
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()


if __name__ == "__main__":
    # Example usage (replace with your actual values)
    PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
    TEXT_TO_CHECK = "You are an idiot!"

    if PERSPECTIVE_API_KEY:
        safety_analysis = check_text_safety(TEXT_TO_CHECK, PERSPECTIVE_API_KEY)
        print("Safety Analysis:\n", safety_analysis)
    else:
        print("Please set PERSPECTIVE_API_KEY.")
