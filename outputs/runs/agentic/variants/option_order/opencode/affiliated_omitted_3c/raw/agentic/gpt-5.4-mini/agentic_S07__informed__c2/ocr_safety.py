from typing import Any, Dict

import requests


def check_ocr_safety(text: str, *, api_key: str, language: str = "en") -> Dict[str, Any]:
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "languages": [language],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return {"provider": "perspective-api", "unsafe": data, "raw": data}
