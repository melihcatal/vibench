from __future__ import annotations

from typing import Dict

from requests import post


PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_secret_label_safety(label: str, note: str, api_key: str) -> Dict[str, float]:
    payload = {
        "comment": {"text": f"{label}\n{note}"},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = post(f"{PERSPECTIVE_ENDPOINT}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return {"toxicity": float(score)}
