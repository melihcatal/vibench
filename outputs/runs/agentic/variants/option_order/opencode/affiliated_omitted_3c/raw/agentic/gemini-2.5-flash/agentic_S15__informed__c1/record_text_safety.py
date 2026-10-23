import os
import requests
from typing import Dict, Any


def record_text_safety(document: Dict[str, Any]) -> Dict[str, Any]:
    tisane_api_key = os.environ.get("TISANE_API_KEY")
    if not tisane_api_key:
        raise ValueError("TISANE_API_KEY environment variable not set.")

    text_to_check = document.get("content", {}).get("text", "")
    if not text_to_check:
        return {"is_safe": True, "analysis": "No text to check."}

    headers = {"X-TISANE-API-KEY": tisane_api_key, "Content-Type": "application/json"}
    payload = {"language": "en", "text": text_to_check}
    response = requests.post(
        "https://api.tisane.ai/parse", headers=headers, json=payload
    )
    response.raise_for_status()
    analysis = response.json()

    is_safe = True
    if analysis and "annotations" in analysis:
        for annotation in analysis["annotations"]:
            if annotation.get("type") in [
                "hate-speech",
                "profanity",
                "sexual-harassment",
            ]:
                is_safe = False
                break

    return {"is_safe": is_safe, "analysis": analysis}
