from typing import Dict, List, Optional
import os
import requests


def ocr_safety(text: str) -> Dict:
    """
    Checks extracted document text for unsafe content using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    if not api_key:
        raise ValueError("Perspective API key not configured.")

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

    result = response.json()

    attributes = {}
    for attribute in data["requestedAttributes"].keys():
        score = result["attributeScores"][attribute]["summaryScore"]["value"]
        attributes[attribute.lower()] = score

    return {
        "safe": all(score < 0.7 for score in attributes.values()),
        "scores": attributes,
    }
