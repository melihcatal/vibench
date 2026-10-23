import os
import requests
from typing import Dict, Any


def moderate_text_with_perspective(text: str) -> Dict[str, Any]:
    """
    Moderates free-text claims or notes using the Perspective API.
    """
    PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is not set.")

    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    example_claim = "This user is great and helpful!"
    # example_claim = "You are an idiot!" # Uncomment to test a more toxic example

    print(f"Moderating text: '{example_claim}' with Perspective API...")
    # Ensure PERSPECTIVE_API_KEY is set in your environment
    moderation_result = moderate_text_with_perspective(example_claim)
    print("\n--- Moderation Result ---")
    print(moderation_result)

    if "attributeScores" in moderation_result:
        for attribute, scores in moderation_result["attributeScores"].items():
            print(f"{attribute}: {scores['summaryScore']['value']:.2f}")
