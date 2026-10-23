import os
import json
import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_message_safety(
    text: str,
    attributes: list[str] | None = None,
    threshold: float = 0.7,
) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    if attributes is None:
        attributes = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "INSULT",
            "PROFANITY",
            "THREAT",
        ]

    requested_attrs = {attr: {} for attr in attributes}

    payload = {
        "comment": {"text": text},
        "requestedAttributes": requested_attrs,
        "languages": ["en"],
    }

    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json=payload,
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    attribute_scores = {}
    flagged = False
    for attr_name, attr_data in data.get("attributeScores", {}).items():
        score = attr_data.get("summaryScore", {}).get("value", 0.0)
        attribute_scores[attr_name] = round(score, 4)
        if score >= threshold:
            flagged = True

    return {
        "text_length": len(text),
        "flagged": flagged,
        "threshold": threshold,
        "attribute_scores": attribute_scores,
        "status": "safe" if not flagged else "unsafe",
        "provider": "Perspective API",
    }


if __name__ == "__main__":
    sample_text = "This is a perfectly normal and friendly message."
    result = check_message_safety(sample_text)
    print(json.dumps(result, indent=2))
