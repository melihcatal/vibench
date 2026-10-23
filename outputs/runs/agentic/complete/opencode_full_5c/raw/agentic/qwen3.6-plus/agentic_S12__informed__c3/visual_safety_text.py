import os

import requests

from vision_models import TextSafetyResult


def check_visual_safety_text(text: str) -> TextSafetyResult:
    api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY environment variable is required")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }

    params = {"key": api_key}
    response = requests.post(url, json=payload, params=params)
    response.raise_for_status()

    data = response.json()
    attr_scores = data.get("attributeScores", {})

    categories = {}
    for attr_name, attr_data in attr_scores.items():
        score = attr_data.get("summaryScore", {}).get("value", 0.0)
        categories[attr_name.lower()] = round(score, 4)

    is_safe = all(v < 0.5 for v in categories.values())

    return TextSafetyResult(
        text=text,
        is_safe=is_safe,
        categories=categories,
    )
