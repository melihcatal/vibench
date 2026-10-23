from typing import Iterable, Mapping

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_text_safety(text_fields: Iterable[Mapping[str, str]], api_key: str) -> dict:
    comments = "\n".join(field.get("text", "") for field in text_fields)
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": comments},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
