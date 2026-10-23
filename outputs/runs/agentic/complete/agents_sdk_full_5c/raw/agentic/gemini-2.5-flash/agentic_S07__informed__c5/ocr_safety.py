import os
import requests
from document_models import OcrSafetyRequest, OcrSafetyResponse

def check_ocr_safety(request: OcrSafetyRequest) -> OcrSafetyResponse:
    """Checks extracted document text for unsafe content using Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    # The attributes to analyze for content safety
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {}
    }

    payload = {
        "comment": {
            "text": request.text_content
        },
        "requestedAttributes": requested_attributes
    }

    response = requests.post(url, json=payload)
    response.raise_for_status() # Raise an exception for HTTP errors

    result = response.json()
    safety_scores = {}

    for attribute, data in result.get("attributeScores", {}).items():
        safety_scores[attribute] = data["summaryScore"]["value"]

    return OcrSafetyResponse(safety_scores=safety_scores)
