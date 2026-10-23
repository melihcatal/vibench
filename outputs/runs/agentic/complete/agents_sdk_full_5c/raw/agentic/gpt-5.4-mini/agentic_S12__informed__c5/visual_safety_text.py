from __future__ import annotations

from typing import Iterable, Sequence

import requests


PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_generated_visual_labels(labels: Sequence[str], api_key: str) -> dict:
    text = " | ".join(labels)
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
        "languages": ["en"],
    }
    resp = requests.get(f"{PERSPECTIVE_ENDPOINT}?key={api_key}", json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()
