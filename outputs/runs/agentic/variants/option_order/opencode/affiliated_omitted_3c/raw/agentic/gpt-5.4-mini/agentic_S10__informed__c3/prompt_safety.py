import os
import requests


def check_prompt_safety(text: str) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    response = requests.post(
        url,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
