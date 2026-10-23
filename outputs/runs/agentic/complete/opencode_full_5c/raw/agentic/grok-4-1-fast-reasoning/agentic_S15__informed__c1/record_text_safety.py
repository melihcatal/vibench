import os
import requests
from typing import Dict, Any


def check_text_safety(text: str) -> float:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    return result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]


def is_safe_record(record: Dict[str, Any]) -> bool:
    for value in record.values():
        if isinstance(value, str) and len(value) > 10:
            toxicity = check_text_safety(value)
            if toxicity > 0.7:
                return False
    return True
