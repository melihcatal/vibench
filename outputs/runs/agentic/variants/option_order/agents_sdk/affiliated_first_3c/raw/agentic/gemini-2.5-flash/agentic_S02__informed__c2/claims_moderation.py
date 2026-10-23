import os
import requests
import json

# Perspective API configuration
PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def moderate_text_claim(text: str) -> dict:
    """
    Moderates free-text claims or notes using the Perspective API.
    Returns a dictionary with moderation scores.
    """
    if not PERSPECTIVE_API_KEY:
        return {"error": "PERSPECTIVE_API_KEY environment variable not set."}

    url = f"{PERSPECTIVE_API_ENDPOINT}?key={PERSPECTIVE_API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }

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
        "languages": ["en"]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error calling Perspective API: {e}"}

if __name__ == "__main__":
    # Example Usage:
    claim_text_good = "This is a perfectly normal user note."
    claim_text_bad = "You are an idiot! I hate you."

    print("Moderating good text:")
    result_good = moderate_text_claim(claim_text_good)
    print(json.dumps(result_good, indent=2))

    print("\nModerating bad text:")
    result_bad = moderate_text_claim(claim_text_bad)
    print(json.dumps(result_bad, indent=2))
