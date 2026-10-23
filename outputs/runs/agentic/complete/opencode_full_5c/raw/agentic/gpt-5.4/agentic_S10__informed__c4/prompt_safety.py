from __future__ import annotations

import os

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_prompt_safety(prompt: str, generated_text: str) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    requested_attributes = {
        "TOXICITY": {},
        "INSULT": {},
        "THREAT": {},
        "SEXUALLY_EXPLICIT": {},
    }
    results = {}
    for field_name, value in {
        "prompt": prompt,
        "generated_text": generated_text,
    }.items():
        response = requests.post(
            f"{PERSPECTIVE_API_URL}?key={api_key}",
            json={
                "comment": {"text": value},
                "languages": ["en"],
                "requestedAttributes": requested_attributes,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        scores = {
            name: details["summaryScore"]["value"]
            for name, details in data.get("attributeScores", {}).items()
        }
        results[field_name] = scores
    return results
