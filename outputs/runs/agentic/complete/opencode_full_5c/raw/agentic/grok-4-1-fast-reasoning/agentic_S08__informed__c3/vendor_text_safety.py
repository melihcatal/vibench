import os
import requests
import json


def moderate_vendor_text(text: str) -> dict:
    """
    Moderate vendor notes using Google Perspective API for toxicity.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY required.")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {},
        },
        "doNotStore": True,
    }

    response = requests.post(f"{url}?key={api_key}", json=payload)
    response.raise_for_status()
    result = response.json()

    scores = {
        k: v["summaryScore"]["value"]
        for k, v in result.get("attributeScores", {}).items()
    }

    is_safe = all(
        scores.get(k, 0.0) < 0.5
        for k in ["TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK", "THREAT"]
    )

    return {
        "safe": is_safe,
        "scores": scores,
        "analyzed_text": text[:200] + "..." if len(text) > 200 else text,
    }
