import os
from typing import Dict

import requests


def check_unsafe_copy(text: str) -> Dict[str, str]:
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
