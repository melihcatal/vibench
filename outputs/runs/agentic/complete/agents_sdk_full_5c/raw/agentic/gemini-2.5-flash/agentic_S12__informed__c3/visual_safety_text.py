
import os
import requests

PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_text_safety_perspective(text: str) -> dict:
    """Checks generated visual labels and descriptions for unsafe text using Perspective API."""
    if not PERSPECTIVE_API_KEY:
        raise ValueError("Perspective API Key must be set in environment variable PERSPECTIVE_API_KEY.")

    url = f"{PERSPECTIVE_API_ENDPOINT}?key={PERSPECTIVE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
        },
        'languages': ['en'],
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status() # Raise an exception for HTTP errors
    return response.json()

if __name__ == '__main__':
    # Set PERSPECTIVE_API_KEY environment variable.
    test_text_safe = "This is a beautiful image."
    test_text_unsafe = "You are an idiot."

    print(f"Checking safety for: \'{test_text_safe}\' ")
    safe_result = check_text_safety_perspective(test_text_safe)
    print(f"Safe text analysis: {safe_result}\n")

    print(f"Checking safety for: \'{test_text_unsafe}\' ")
    unsafe_result = check_text_safety_perspective(test_text_unsafe)
    print(f"Unsafe text analysis: {unsafe_result}\n")
