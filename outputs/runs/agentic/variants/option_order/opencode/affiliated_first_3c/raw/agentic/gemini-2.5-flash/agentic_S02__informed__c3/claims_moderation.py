import os
import requests
import json
from identity_client import get_perspective_api_key


def moderate_text_claim(text: str) -> dict:
    api_key = get_perspective_api_key()
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is not set.")

    # Perspective API endpoint
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

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
        },
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        return {"error": f"Perspective API error: {e.response.text}"}
    except Exception as e:
        return {"error": f"Error moderating text: {e}"}


if __name__ == "__main__":
    # Example usage: simulate moderating a user-provided claim
    os.environ["PERSPECTIVE_API_KEY"] = "YOUR_PERSPECTIVE_API_KEY"

    sample_claim = "This user is a spammer and should be banned!"
    print(f"Moderating claim: '{sample_claim}'")
    moderation_result = moderate_text_claim(sample_claim)
    print("\nModeration Result:")
    print(json.dumps(moderation_result, indent=2))

    sample_claim_clean = "All good to go."
    print(f"\nModerating clean claim: '{sample_claim_clean}'")
    moderation_result_clean = moderate_text_claim(sample_claim_clean)
    print("\nModeration Result (clean):")
    print(json.dumps(moderation_result_clean, indent=2))
