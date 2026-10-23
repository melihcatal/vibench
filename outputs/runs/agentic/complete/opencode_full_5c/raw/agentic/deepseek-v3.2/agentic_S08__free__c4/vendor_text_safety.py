import os
from typing import Dict, List, Any, Optional
import json
import requests


def moderate_vendor_text(
    vendor_text: str, notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Moderate vendor notes or memo fields using Google Cloud Perspective API.
    """
    api_key = os.getenv("GOOGLE_PERSPECTIVE_API_KEY")

    if not api_key:
        raise ValueError("Google Perspective API key not configured")

    text_to_analyze = vendor_text
    if notes:
        text_to_analyze = f"{vendor_text}. {notes}"

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
        "comment": {"text": text_to_analyze},
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

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    result = response.json()

    moderation_scores = {}
    for attribute_name, attribute_data in result.get("attributeScores", {}).items():
        score = attribute_data.get("summaryScore", {}).get("value", 0.0)
        moderation_scores[attribute_name.lower()] = score

    is_safe = all(score < 0.7 for score in moderation_scores.values())

    flagged_attributes = [
        attr for attr, score in moderation_scores.items() if score >= 0.7
    ]

    overall_risk_score = max(moderation_scores.values()) if moderation_scores else 0.0

    risk_level = "low"
    if overall_risk_score >= 0.9:
        risk_level = "critical"
    elif overall_risk_score >= 0.7:
        risk_level = "high"
    elif overall_risk_score >= 0.4:
        risk_level = "medium"

    moderation_result = {
        "is_safe": is_safe,
        "risk_level": risk_level,
        "overall_risk_score": overall_risk_score,
        "moderation_scores": moderation_scores,
        "flagged_attributes": flagged_attributes,
        "text_length": len(text_to_analyze),
        "provider": "google_perspective_api",
        "analyzed_at": json.dumps({"timestamp": "2024-01-01T00:00:00Z"}),  # Placeholder
    }

    if not is_safe:
        moderation_result["recommendation"] = (
            "Review vendor text for inappropriate content"
        )
        moderation_result["action_required"] = True
    else:
        moderation_result["recommendation"] = "Vendor text appears appropriate"
        moderation_result["action_required"] = False

    return moderation_result
