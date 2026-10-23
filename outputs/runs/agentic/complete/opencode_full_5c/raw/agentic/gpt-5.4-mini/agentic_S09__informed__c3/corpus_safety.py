import os

import requests


def corpus_safety(texts):
    endpoint = os.environ.get(
        "PERSPECTIVE_API_ENDPOINT",
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
    )
    api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
    results = []
    for text in texts:
        response = requests.post(
            endpoint,
            params={"key": api_key},
            json={
                "comment": {"text": text},
                "languages": ["en"],
                "requestedAttributes": {"TOXICITY": {}},
            },
            timeout=30,
        )
        response.raise_for_status()
        results.append(response.json())
    return results
