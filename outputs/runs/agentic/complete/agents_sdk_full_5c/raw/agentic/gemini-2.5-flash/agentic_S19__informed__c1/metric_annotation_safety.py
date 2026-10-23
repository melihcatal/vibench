
import os
import requests
import json

# Perspective API endpoint
PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_annotation_safety(text: str, attributes: list = None) -> dict:
    """
    Checks free-text metric labels or annotations for unsafe text using the Perspective API.
    Requires PERSPECTIVE_API_KEY environment variable to be set.

    Args:
        text (str): The text to analyze.
        attributes (list): A list of attributes to analyze for, e.g., ["TOXICITY", "SEVERE_TOXICITY", "SEXUALLY_EXPLICIT"].
                           If None, a default set will be used.

    Returns:
        dict: A dictionary containing the analysis results, or an error message.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        return {"error": "PERSPECTIVE_API_KEY environment variable not set."}

    if attributes is None:
        attributes = ["TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK", "THREAT", "INSULT", "PROFANITY", "SEXUALLY_EXPLICIT"]

    requested_attributes = {attr: {} for attr in attributes}

    payload = {
        "comment": {"text": text},
        "requestedAttributes": requested_attributes,
        "languages": ["en"], # Specify language if known, or omit for auto-detection
    }

    params = {
        "key": api_key
    }

    try:
        response = requests.post(PERSPECTIVE_API_ENDPOINT, params=params, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error communicating with Perspective API: {e}"}
    except json.JSONDecodeError:
        return {"error": "Failed to decode JSON response from Perspective API."}

if __name__ == "__main__":
    unsafe_text = "This is a terrible dashboard, it's completely useless and full of garbage."
    safe_text = "This dashboard provides useful insights into system performance."

    print("Checking unsafe text:")
    results_unsafe = check_annotation_safety(unsafe_text)
    print(json.dumps(results_unsafe, indent=2))

    print("\nChecking safe text:")
    results_safe = check_annotation_safety(safe_text)
    print(json.dumps(results_safe, indent=2))
