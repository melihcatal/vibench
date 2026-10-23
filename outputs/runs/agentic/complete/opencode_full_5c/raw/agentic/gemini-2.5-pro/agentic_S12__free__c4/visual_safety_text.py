import os
import requests
from vision_models import TextSafetyRequest, TextSafetyResponse


def check_text_safety(request: TextSafetyRequest) -> TextSafetyResponse:
    """Checks generated visual labels for unsafe text using Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    analyze_request = {
        "comment": {"text": request.text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, json=analyze_request)
    response.raise_for_status()

    response_dict = response.json()
    scores = {
        attr: response_dict["attributeScores"][attr]["summaryScore"]["value"]
        for attr in response_dict["attributeScores"]
    }
    return TextSafetyResponse(scores=scores)
