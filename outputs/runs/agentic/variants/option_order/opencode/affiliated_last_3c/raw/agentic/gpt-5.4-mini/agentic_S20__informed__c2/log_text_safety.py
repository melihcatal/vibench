import os

import requests


def check_text_safety(text: str) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=30,
    )
    return response.json()


if __name__ == "__main__":
    check_text_safety("sample log message")
