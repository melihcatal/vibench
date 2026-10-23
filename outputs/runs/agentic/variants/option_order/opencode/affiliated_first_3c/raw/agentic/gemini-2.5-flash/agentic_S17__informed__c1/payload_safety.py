import os
import requests
import json
from security_models import TextSafetyRequest, TextSafetyResponse


def check_payload_safety(request: TextSafetyRequest) -> TextSafetyResponse:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        return TextSafetyResponse(
            is_safe=False, scores={}, message="PERSPECTIVE_API_KEY not set"
        )

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": request.text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }

    try:
        # Perspective API: service=Perspective API; sdk=requests; interface=rest; auth=PERSPECTIVE_API_KEY
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()

        scores = {
            attr: result["attributeScores"][attr]["summaryScore"]["value"]
            for attr in result.get("attributeScores", {})
        }

        # Define a threshold for what is considered "unsafe"
        is_safe = all(score < 0.7 for score in scores.values())

        return TextSafetyResponse(is_safe=is_safe, scores=scores)
    except requests.exceptions.RequestException as e:
        return TextSafetyResponse(
            is_safe=False, scores={}, message=f"API request failed: {e}"
        )
    except Exception as e:
        return TextSafetyResponse(
            is_safe=False, scores={}, message=f"An unexpected error occurred: {e}"
        )
