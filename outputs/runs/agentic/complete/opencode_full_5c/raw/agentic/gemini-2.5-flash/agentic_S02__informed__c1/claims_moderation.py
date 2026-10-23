import os
import requests
import json
from typing import Dict, Any

# Perspective API endpoint (Google Cloud)
# https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze


def moderate_claims_text(text: str) -> Dict[str, Any]:
    """Moderates free-text claims or notes using the Perspective API."""
    perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not perspective_api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={perspective_api_key}"

    headers = {"Content-Type": "application/json"}

    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
            "INSULT": {},
            "PROFANITY": {},
        },
    }

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        print(f"Response content: {response.text if response else 'No response'}")
        return {"error": str(e), "response_content": response.text if response else ""}


if __name__ == "__main__":
    # Example usage
    # os.environ["PERSPECTIVE_API_KEY"] = "YOUR_PERSPECTIVE_API_KEY"
    #
    # test_text_clean = "This is a perfectly fine and friendly comment."
    # test_text_toxic = "You are an idiot!"
    #
    # try:
    #     print("\nModerating clean text:")
    #     result_clean = moderate_claims_text(test_text_clean)
    #     print(json.dumps(result_clean, indent=2))
    #
    #     print("\nModerating toxic text:")
    #     result_toxic = moderate_claims_text(test_text_toxic)
    #     print(json.dumps(result_toxic, indent=2))
    # except ValueError as e:
    #     print(f"Error: {e}")
    pass  # placeholder to avoid runtime error if __name__ is run without actual env vars
