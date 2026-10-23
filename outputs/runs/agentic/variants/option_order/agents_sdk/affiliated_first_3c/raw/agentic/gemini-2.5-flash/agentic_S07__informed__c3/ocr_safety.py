import os
import requests
from document_models import SafetyAnalysisResponse

PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_content_safety(text: str) -> SafetyAnalysisResponse:
    """
    Checks extracted document text for unsafe content using Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{PERSPECTIVE_API_ENDPOINT}?key={api_key}"
    
    request_body = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, json=request_body)
    response.raise_for_status()
    
    analysis_result = response.json()
    
    scores = {}
    is_safe = True
    for attribute, result in analysis_result.get("attributeScores", {}).items():
        score_value = result.get("summaryScore", {}).get("value", 0.0)
        scores[attribute] = score_value
        if score_value > 0.5:  # Example threshold for unsafe content
            is_safe = False
            
    return SafetyAnalysisResponse(is_safe=is_safe, scores=scores)

