from __future__ import annotations

import os

import requests

from vision_models import LabelResult

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY", "")
PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_label_text_safety(labels):
    text = ", ".join(label.name if isinstance(label, LabelResult) else str(label) for label in labels)
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(PERSPECTIVE_URL, params={"key": PERSPECTIVE_API_KEY}, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
