import os
from typing import Iterable, List

import requests

PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def corpus_safety(texts: Iterable[str]) -> List[dict]:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    headers = {"Content-Type": "application/json"}
    payload = {
        "comment": {"text": "\n".join(texts)},
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        "doNotStore": True,
        "languages": ["en"],
    }
    response = requests.post(f"{PERSPECTIVE_API_HOST}?key={api_key}", headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return [{"attribute": k, "score": v["summaryScore"]["value"]} for k, v in data.get("attributeScores", {}).items()]
