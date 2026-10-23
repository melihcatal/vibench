import os
import requests
from typing import Dict, List, Any


def check_content_safety(text: str) -> Dict[str, Any]:
    """Check narration scripts for unsafe content using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    params = {"key": api_key}

    payload = {
        "comment": {"text": text},
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

    response = requests.post(url, params=params, json=payload)
    response.raise_for_status()

    result = response.json()

    scores = {}
    for attribute_name, attribute_data in result.get("attributeScores", {}).items():
        scores[attribute_name] = attribute_data.get("summaryScore", {}).get(
            "value", 0.0
        )

    return {
        "scores": scores,
        "languages": result.get("languages", []),
        "detected_languages": result.get("detectedLanguages", []),
    }


def check_batch_safety(texts: List[str]) -> List[Dict[str, Any]]:
    """Check multiple narration scripts for unsafe content using Perspective API."""
    results = []
    for text in texts:
        try:
            result = check_content_safety(text)
            results.append(result)
        except Exception as e:
            results.append({"error": str(e), "text": text[:100]})

    return results


def get_safety_recommendation(scores: Dict[str, float], threshold: float = 0.7) -> str:
    """Get safety recommendation based on content safety scores."""
    high_risk_attributes = []
    for attribute, score in scores.items():
        if score >= threshold:
            high_risk_attributes.append(attribute)

    if high_risk_attributes:
        return f"Content contains potentially unsafe attributes: {', '.join(high_risk_attributes)}"
    else:
        return "Content appears safe for narration"
