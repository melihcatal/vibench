import os
from typing import Dict

import requests


def check_ocr_safety(text: str) -> Dict[str, object]:
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={"comment": {"text": text}, "languages": ["en"], "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}, "THREAT": {}}},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
