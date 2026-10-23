from typing import Dict, List
import requests
from document_models import OCRResponse


def ocr_safety(text: str) -> Dict[str, bool]:
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

    attribute_scores = response.json()["attributeScores"]
    results = {}

    for attribute in attribute_scores:
        score = attribute_scores[attribute]["summaryScore"]["value"]
        results[attribute.lower()] = score > 0.7

    return results
