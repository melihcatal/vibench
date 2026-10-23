import os
import requests
import json
from typing import Dict, Any, Optional

# Perspective API endpoint and discovery URL
# https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1
PERSP_API_BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_content_safety(text_content: str) -> Optional[Dict[str, Any]]:
    """Checks message payload text for unsafe content using Perspective API."""
    perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not perspective_api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{PERSP_API_BASE_URL}?key={perspective_api_key}"

    # Define the attributes to analyze. You can add more as needed.
    # See https://developers.perspectiveapi.com/s/about-the-api-attributes for full list.
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
    }

    payload = {
        "comment": {"text": text_content},
        "languages": ["en"],
        "requestedAttributes": requested_attributes,
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        analysis_result = response.json()

        # Extract relevant scores
        scores = {}
        for attr, data in analysis_result.get("attributeScores", {}).items():
            scores[attr] = data.get("summaryScore", {}).get("value")
        return scores

    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        if e.response:
            print(f"Response content: {e.response.text}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    # Example usage:
    # Set PERSPECTIVE_API_KEY environment variable.
    # export PERSPECTIVE_API_KEY="YOUR_PERSPECTIVE_API_KEY"

    example_text_safe = "This is a perfectly fine message."
    example_text_unsafe = "You are an idiot! I hate you!"

    print("\n--- Checking safe text ---")
    safe_scores = check_content_safety(example_text_safe)
    if safe_scores:
        print(json.dumps(safe_scores, indent=2))

    print("\n--- Checking unsafe text ---")
    unsafe_scores = check_content_safety(example_text_unsafe)
    if unsafe_scores:
        print(json.dumps(unsafe_scores, indent=2))
