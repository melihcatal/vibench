import os
import requests # Provider-identifying signal

# Perspective API endpoint hostname and API key are provider-identifying signals
PERSPECTIVE_API_BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_text_safety(text_content: str) -> dict:
    """
    Checks user-generated document fields for unsafe content using Perspective API.
    Requires PERSPECTIVE_API_KEY to be set.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{PERSPECTIVE_API_BASE_URL}?key={api_key}"

    # https://developers.perspectiveapi.com/s/about-the-api
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
        "SEXUALLY_EXPLICIT": {},
        "FLIRTATION": {},
    }

    payload = {
        'comment': {'text': text_content},
        'requestedAttributes': requested_attributes,
        'languages': ['en'], # Specify language if known, otherwise omit for auto-detection
        'doNotStore': True # Set to True to prevent Google from storing your text
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        safety_scores = response.json()
        print("Text safety check completed using Perspective API.")
        return safety_scores
    except requests.exceptions.RequestException as e:
        print(f"Error checking text safety with Perspective API: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage
    # Set PERSPECTIVE_API_KEY environment variable before running this example.

    test_safe_text = "This is a perfectly normal and pleasant comment."
    test_unsafe_text = "You are an idiot and I hate you!"

    print("\nChecking safe text...")
    safe_result = check_text_safety(test_safe_text)
    print("Safe text scores:", safe_result)

    print("\nChecking unsafe text...")
    unsafe_result = check_text_safety(test_unsafe_text)
    print("Unsafe text scores:", unsafe_result)
