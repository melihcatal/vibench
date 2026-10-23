import os
import requests
from security_models import TextPayload, SafetyCheckResponse


def check_payload_safety(payload: TextPayload) -> SafetyCheckResponse:
    """Checks decrypted text payloads for unsafe content using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        return SafetyCheckResponse(
            is_safe=False, scores={"error": "PERSPECTIVE_API_KEY not set."}
        )

    # Perspective API: service=Perspective API; sdk=requests; interface=rest; auth=PERSPECTIVE_API_KEY
    url = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + api_key
    )
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": payload.text},
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
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        scores = {
            attr: result["attributeScores"][attr]["summaryScore"]["value"]
            for attr in data["requestedAttributes"].keys()
        }

        # Define a threshold for what is considered 'unsafe'
        # This is an example; actual thresholds might vary based on requirements.
        is_safe = all(score < 0.7 for score in scores.values())  # Example threshold

        return SafetyCheckResponse(is_safe=is_safe, scores=scores)

    except requests.exceptions.RequestException as e:
        return SafetyCheckResponse(is_safe=False, scores={"error": str(e)})
