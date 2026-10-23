import requests
import os
from typing import Dict, Any

# Perspective API base URL
PERSPECTIVE_API_BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def analyze_text_for_safety(text: str, api_key: str) -> Dict[str, Any]:
    """Checks text for unsafe content using Google Perspective API."""
    params = {
        "key": api_key
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "comment": {
            "text": text
        },
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"]
    }

    try:
        response = requests.post(PERSPECTIVE_API_BASE_URL, params=params, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not perspective_api_key:
        print("Please set the PERSPECTIVE_API_KEY environment variable.")
    else:
        text_to_check_safe = "This is a perfectly normal and safe sentence."
        result_safe = analyze_text_for_safety(text_to_check_safe, perspective_api_key)
        print(f"\nSafety analysis for: '{text_to_check_safe}'")
        for attribute, score_info in result_safe.get("attributeScores", {}).items():
            print(f"  {attribute}: {score_info["summaryScore"]["value"]:.4f}")

        text_to_check_unsafe = "You are an idiot and I will hurt you!"
        result_unsafe = analyze_text_for_safety(text_to_check_unsafe, perspective_api_key)
        print(f"\nSafety analysis for: '{text_to_check_unsafe}'")
        for attribute, score_info in result_unsafe.get("attributeScores", {}).items():
            print(f"  {attribute}: {score_info["summaryScore"]["value"]:.4f}")
