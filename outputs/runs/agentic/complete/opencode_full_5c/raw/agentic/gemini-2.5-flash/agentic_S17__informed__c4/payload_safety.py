import os
import requests
import json

# NOTE: PERSPECTIVE_API_KEY should be set as an environment variable
# The API endpoint below is a placeholder. A real implementation would use the actual Discovery API to find the endpoint or a hardcoded one if known.


def check_payload_safety(text_payload: str) -> dict:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # The actual Perspective API endpoint is usually found via the Discovery API or is a known URL.
    # For this example, we'll use a representative URL structure.
    # https://developers.perspectiveapi.com/s/docs-sample-requests
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text_payload},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking payload safety with Perspective API: {e}")
        return {"error": str(e)}
