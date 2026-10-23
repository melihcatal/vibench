import os
import requests


def check_localized_copy_safety(text: str, language_code: str = "es") -> dict:
    """Check localized copy for unsafe content using Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
        "comment": {"text": text},
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

    safety_summary = {
        "text": text,
        "language": language_code,
        "scores": {},
        "is_safe": True,
        "unsafe_attributes": [],
    }

    for attribute_name, attribute_data in result.get("attributeScores", {}).items():
        score = attribute_data.get("summaryScore", {}).get("value", 0)
        safety_summary["scores"][attribute_name] = score

        if score > 0.7:
            safety_summary["is_safe"] = False
            safety_summary["unsafe_attributes"].append(attribute_name)

    return safety_summary
