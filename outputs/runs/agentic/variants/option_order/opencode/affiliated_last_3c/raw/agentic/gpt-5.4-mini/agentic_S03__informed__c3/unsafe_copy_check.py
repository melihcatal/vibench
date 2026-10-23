from typing import Dict

import requests


PERSPECTIVE_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def unsafe_copy_check(text: str) -> Dict[str, float]:
    api_key = requests.utils.default_headers().get("PERSPECTIVE_API_KEY")
    params = {"key": api_key}
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(PERSPECTIVE_HOST, params=params, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return {
        "toxicity": data["attributeScores"]["TOXICITY"]["summaryScore"]["value"],
        "provider": 0.0,
    }
