import os
import requests
from vision_models import VisualSafetyTextRequest, VisualSafetyTextResponse


def visual_safety_text(request: VisualSafetyTextRequest) -> VisualSafetyTextResponse:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    # The request should be a list of one or more text entries to analyze.
    # In this case, we have a single text string from the request.
    # See https://developers.perspectiveapi.com/s/docs-sample-requests for examples of valid request bodies.
    data = {
        "comment": {"text": request.text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
            "ATTACK_ON_AUTHOR": {},
            "ATTACK_ON_TARGET": {},
        },
    }

    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()

    is_safe = True
    scores = {}
    for attribute, details in result.get("attributeScores", {}).items():
        score_value = details.get("summaryScore", {}).get("value")
        scores[attribute] = score_value
        # Define a threshold for safety. This is an example, adjust as needed.
        if (
            score_value and score_value > 0.5
        ):  # If any score is above 0.5, consider it unsafe
            is_safe = False

    return VisualSafetyTextResponse(is_safe=is_safe, scores=scores)
