from typing import Dict, List
import requests
from document_models import OCRResponse


def check_unsafe_content(text: str) -> Dict:
    """Check extracted document text for unsafe content using Perspective API."""
    api_key = "PERSPECTIVE_API_KEY"  # Replace with environment variable in production
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    data = {
        "comment": {"text": text},
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

    response = requests.post(url, json=data)
    response.raise_for_status()

    return response.json()


def ocr_safety(ocr_response: OCRResponse) -> Dict:
    """Check extracted document text for unsafe content."""
    safety_results = check_unsafe_content(ocr_response.full_text)

    return {
        "text": ocr_response.full_text,
        "safety_scores": safety_results.get("attributeScores", {}),
        "provider": "perspective",
        "model": "perspective_api",
    }
