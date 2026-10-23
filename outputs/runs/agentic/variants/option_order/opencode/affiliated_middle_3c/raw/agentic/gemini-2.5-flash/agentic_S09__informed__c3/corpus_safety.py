import os
import requests
from typing import List, Dict, Any

PERSPECTIVE_API_BASE_URL = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def check_text_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    params = {"key": api_key}
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

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(
            PERSPECTIVE_API_BASE_URL, params=params, json=data, headers=headers
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def check_corpus_safety(corpus: List[str]) -> List[Dict[str, Any]]:
    safety_reports = []
    for text in corpus:
        report = check_text_safety(text)
        safety_reports.append({"text": text, "safety_report": report})
    return safety_reports
