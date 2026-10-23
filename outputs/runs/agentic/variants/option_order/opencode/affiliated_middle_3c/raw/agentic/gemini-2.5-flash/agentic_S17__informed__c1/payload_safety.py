import os
import requests
import json
from security_models import PayloadSafetyRequest, PayloadSafetyResponse


def check_payload_safety(request: PayloadSafetyRequest) -> PayloadSafetyResponse:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": request.decrypted_payload},
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
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()

        scores = {
            attr: result["attributeScores"][attr]["summaryScore"]["value"]
            for attr in data["requestedAttributes"]
        }

        # Define a simple safety threshold. Adjust as needed.
        is_safe = all(score < 0.7 for score in scores.values())  # Example threshold

        return PayloadSafetyResponse(is_safe=is_safe, scores=scores)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to check payload safety with Perspective API: {e}")
