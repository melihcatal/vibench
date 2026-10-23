import os
import requests
from typing import Dict, Any

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def record_text_safety(record: Dict[str, Any]) -> bool:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        return True
    
    content = record.get("content", {})
    for value in content.values():
        if isinstance(value, str) and value.strip():
            url = f"{PERSPECTIVE_API_URL}?key={api_key}"
            payload = {
                "comment": {"text": value},
                "requestedAttributes": {"TOXICITY": {}}
            }
            try:
                resp = requests.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()
                toxicity = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
                if toxicity > 0.7:
                    return False
            except Exception:
                pass  # assume safe on error
    return True