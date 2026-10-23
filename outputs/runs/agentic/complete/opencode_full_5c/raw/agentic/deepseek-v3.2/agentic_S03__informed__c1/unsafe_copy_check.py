import os
import requests
from typing import Dict, Any, List


def check_localized_copy_for_unsafe_content(
    text: str, language_code: str = "en"
) -> Dict[str, Any]:
    """Check localized copy for unsafe content using Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
        "comment": {"text": text, "type": "PLAIN_TEXT"},
        "languages": [language_code],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()

    attribute_scores = {}
    for attr_name, attr_data in result.get("attributeScores", {}).items():
        attribute_scores[attr_name] = {
            "score": attr_data.get("summaryScore", {}).get("value", 0),
            "span_scores": [
                {
                    "begin": score.get("begin", 0),
                    "end": score.get("end", 0),
                    "score": score.get("score", {}).get("value", 0),
                }
                for score in attr_data.get("spanScores", [])
            ],
        }

    overall_risk = any(score["score"] > 0.7 for score in attribute_scores.values())

    return {
        "text": text,
        "language_code": language_code,
        "attribute_scores": attribute_scores,
        "overall_unsafe": overall_risk,
        "high_risk_attributes": [
            attr for attr, data in attribute_scores.items() if data["score"] > 0.7
        ],
    }
