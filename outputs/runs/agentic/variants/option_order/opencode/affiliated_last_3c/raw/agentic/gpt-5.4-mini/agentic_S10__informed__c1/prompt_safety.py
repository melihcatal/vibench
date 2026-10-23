import os

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_prompt_safety(text: str) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(
        f"{PERSPECTIVE_API_URL}?key={api_key}", json=payload, timeout=30
    )
    response.raise_for_status()
    return response.json()


def check_generated_text(text: str) -> dict:
    return check_prompt_safety(text)
