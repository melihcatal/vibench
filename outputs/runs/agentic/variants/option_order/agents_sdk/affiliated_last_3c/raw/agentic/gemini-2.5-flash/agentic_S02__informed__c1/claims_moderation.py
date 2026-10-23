import os
import requests
import json
from identity_client import get_perspective_api_config

def moderate_text_claim(text: str):
    config = get_perspective_api_config()
    api_key = config["PERSPECTIVE_API_KEY"]
    endpoint = config["PERSPECTIVE_API_ENDPOINT"]

    if not api_key or api_key == "YOUR_PERSPECTIVE_API_KEY":
        print("Error: PERSPECTIVE_API_KEY is not set or is default. Please configure your API key.")
        return {"error": "API key not configured."}

    url = f"{endpoint}?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "PROFANITY": {}
        },
        "languages": ["en"]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        print("Successfully moderated text claim using Perspective API.")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    sample_claim_text_good = "This is a perfectly normal user note."
    sample_claim_text_bad = "I hate this new feature! It's terrible and offensive."

    print("Moderating good text:")
    result_good = moderate_text_claim(sample_claim_text_good)
    print(json.dumps(result_good, indent=2))

    print("\nModerating bad text:")
    result_bad = moderate_text_claim(sample_claim_text_bad)
    print(json.dumps(result_bad, indent=2))
