import os
import requests
from typing import Dict, Any


def check_text_safety(text_to_check: str) -> Dict[str, Any]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    request_body = {
        "comment": {"text": text_to_check},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = requests.post(url, json=request_body)
    response.raise_for_status()
    return response.json()
