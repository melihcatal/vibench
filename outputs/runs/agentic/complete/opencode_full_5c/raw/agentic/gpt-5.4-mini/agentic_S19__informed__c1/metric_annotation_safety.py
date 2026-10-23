from typing import Any, Dict

import requests


def metric_annotation_safety(text: str) -> Dict[str, Any]:
    response = requests.post(
        "https://api.perspectiveapi.com/v1alpha1/comments:analyze",
        params={"key": __import__("os").environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
