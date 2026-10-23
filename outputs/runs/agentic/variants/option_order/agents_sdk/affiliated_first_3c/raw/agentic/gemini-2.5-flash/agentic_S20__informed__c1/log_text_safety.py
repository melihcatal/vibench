import os
import requests
from typing import Dict, Any
from observability_models import ContentSafetyRequest

# Perspective API Endpoint
PERSPECTIVE_API_BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_log_text_safety(request: ContentSafetyRequest) -> Dict[str, Any]:
    """
    Checks selected log message text for unsafe content using the Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    if not request.text_content:
        return {"error": "No text content provided for safety check."}

    url = f"{PERSPECTIVE_API_BASE_URL}?key={api_key}"

    # https://developers.perspectiveapi.com/s/docs-sample-requests
    payload = {
        "comment": {"text": request.text_content},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": [request.language]
    }

    headers = {"Content-Type": "application/json"}

    print(f"Sending text to Perspective API for safety check (language: {request.language})...")
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()
        print("Perspective API response received.")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e), "detail": response.text if 'response' in locals() else ""}

if __name__ == "__main__":
    # Example usage
    # Set PERSPECTIVE_API_KEY environment variable
    log_message1 = "This is a perfectly normal log message."
    log_message2 = "You are an idiot and your code sucks!"

    safety_request1 = ContentSafetyRequest(text_content=log_message1)
    safety_request2 = ContentSafetyRequest(text_content=log_message2, language="en")

    print("\n--- Checking log message 1 ---")
    result1 = check_log_text_safety(safety_request1)
    print(result1)

    print("\n--- Checking log message 2 ---")
    result2 = check_log_text_safety(safety_request2)
    print(result2)
