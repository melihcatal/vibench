import os
import requests  # requests library for REST API call is the identifying signal
from vision_models import TextSafetyRequest, TextSafetyResult


# Perspective API endpoint and key environment variable are identifying signals.
def check_text_safety(request: TextSafetyRequest) -> TextSafetyResult:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + api_key
    )

    # The model supports several attributes. Focusing on the main ones for general safety.
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
    }

    data = {
        "comment": {"text": request.text},
        "languages": ["en"],  # Assuming English for this example
        "requestedAttributes": requested_attributes,
    }

    response = requests.post(url, json=data)
    response.raise_for_status()  # Raise an exception for HTTP errors

    result = response.json()

    scores = {}
    is_unsafe = False
    for attribute, details in result.get("attributeScores", {}).items():
        score_value = details.get("summaryScore", {}).get("value")
        if score_value is not None:
            scores[attribute] = score_value
            # Simple threshold for unsafety detection
            if score_value > 0.7:  # If any score is above 0.7, consider it unsafe
                is_unsafe = True

    return TextSafetyResult(is_unsafe=is_unsafe, scores=scores)
