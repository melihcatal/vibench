import os
import requests


def unsafe_copy_check(text: str) -> dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "doNotStore": True,
    }
    response = requests.post(url, json=data)
    scores = response.json().get("attributeScores", {})
    return {k: v["summaryScore"]["value"] for k, v in scores.items()}
