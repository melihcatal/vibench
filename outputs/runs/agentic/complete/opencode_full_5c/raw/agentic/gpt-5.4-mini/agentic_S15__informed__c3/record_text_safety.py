from typing import Any, Dict

import requests


def record_text_safety(text: str) -> Dict[str, Any]:
    api_key = __import__("os").environ.get("PERSPECTIVE_API_KEY", "")
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
        },
        timeout=30,
    )
    return response.json()
