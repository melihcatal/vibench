import os

import requests

PERSPECTIVE_API_KEY = os.environ["PERSPECTIVE_API_KEY"]
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_log_text_safety(text: str) -> dict:
    body = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
        },
        "languages": ["en"],
    }
    params = {"key": PERSPECTIVE_API_KEY}
    response = requests.post(
        PERSPECTIVE_API_URL,
        params=params,
        json=body,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {}
    for attr_name, attr_data in data.get("attributeScores", {}).items():
        summary = attr_data.get("summaryScore", {})
        scores[attr_name] = summary.get("value", 0.0)
    unsafe_attributes = {k: v for k, v in scores.items() if v >= 0.5}
    return {
        "text": text,
        "scores": scores,
        "is_unsafe": len(unsafe_attributes) > 0,
        "unsafe_attributes": unsafe_attributes,
    }


if __name__ == "__main__":
    result = check_log_text_safety("This is a normal log message with no issues.")
    print(result)
