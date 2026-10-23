import os
import requests
import json

PERSPECTIVE_API_BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def moderate_text_with_perspective(text: str) -> dict:
    """
    Moderates the given text using Google's Perspective API.

    Args:
        text: The text to moderate.

    Returns:
        A dictionary containing the moderation results from the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{PERSPECTIVE_API_BASE_URL}?key={api_key}"

    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {}
    }

    payload = {
        "comment": {"text": text},
        "requestedAttributes": requested_attributes,
        "languages": ["en"],
        "doNotStore": True # Set to True for non-public content or if privacy is a concern
    }

    headers = {"Content-Type": "application/json"}

    try:
        print(f"Sending text for moderation to Perspective API (first 50 chars): {text[:50]}...")
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        result = response.json()
        print("Moderation results received.")
        return result
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error calling Perspective API: {e}")
    except json.JSONDecodeError:
        raise Exception("Failed to decode JSON response from Perspective API.")

if __name__ == "__main__":
    try:
        # Example usage: Ensure PERSPECTIVE_API_KEY is set
        test_text_toxic = "You are a terrible person and I hate you!"
        moderation_result_toxic = moderate_text_with_perspective(test_text_toxic)
        print("\n--- Moderation Result (Toxic) ---")
        print(json.dumps(moderation_result_toxic, indent=2))

        test_text_neutral = "This is a perfectly normal sentence with no issues."
        moderation_result_neutral = moderate_text_with_perspective(test_text_neutral)
        print("\n--- Moderation Result (Neutral) ---")
        print(json.dumps(moderation_result_neutral, indent=2))

    except Exception as e:
        print(f"Error in moderation: {e}")
