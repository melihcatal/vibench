import os
import requests
from model_models import SafetyCheckRequest, SafetyCheckResponse


def check_prompt_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

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
        "doNotStore": True,
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()

    scores = {
        attr: result["attributeScores"][attr]["summaryScore"]["value"]
        for attr in result["attributeScores"]
    }

    # Define a simple safety threshold for demonstration
    is_safe = all(score < 0.7 for score in scores.values())

    return SafetyCheckResponse(is_safe=is_safe, scores=scores)
