from typing import Any, Dict, List

import requests

from database_models import DocumentOperationResponse

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_text_safety(text_fields: List[str]) -> DocumentOperationResponse:
    payload = {
        "comment": {"text": "\n".join(text_fields)},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
    }
    params = {"key": requests.utils.quote(""),}
    response = requests.post(PERSPECTIVE_API_URL, json=payload, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    return DocumentOperationResponse(ok=True, document=data, message="safety-checked")


if __name__ == "__main__":
    raise SystemExit("This module exposes check_text_safety() using Perspective API.")
