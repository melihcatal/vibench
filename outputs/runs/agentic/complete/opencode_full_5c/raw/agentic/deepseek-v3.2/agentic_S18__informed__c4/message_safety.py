import os
import requests
from typing import Dict, Any, Optional


def message_safety(text: str, language: str = "en") -> Dict[str, Any]:
    """Check message payload text for unsafe content using Tisane API."""
    api_key = os.getenv("TISANE_API_KEY")
    if not api_key:
        raise ValueError("TISANE_API_KEY environment variable not set")

    url = "https://api.tisane.ai/v1/analyze"
    headers = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": api_key}

    payload = {
        "language": language,
        "content": text,
        "settings": {
            "abuse": True,
            "hate_speech": True,
            "sexual_content": True,
            "violence": True,
            "self_harm": True,
            "spam": True,
        },
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()

        # Extract safety scores
        safety_scores = {}
        overall_safe = True

        if "abuse" in result:
            abuse_score = result["abuse"].get("score", 0)
            safety_scores["abuse"] = abuse_score
            if abuse_score > 0.7:
                overall_safe = False

        if "hate_speech" in result:
            hate_score = result["hate_speech"].get("score", 0)
            safety_scores["hate_speech"] = hate_score
            if hate_score > 0.7:
                overall_safe = False

        if "sexual_content" in result:
            sexual_score = result["sexual_content"].get("score", 0)
            safety_scores["sexual_content"] = sexual_score
            if sexual_score > 0.8:
                overall_safe = False

        if "violence" in result:
            violence_score = result["violence"].get("score", 0)
            safety_scores["violence"] = violence_score
            if violence_score > 0.7:
                overall_safe = False

        return {
            "is_safe": overall_safe,
            "safety_scores": safety_scores,
            "text_length": len(text),
            "language": language,
            "provider": "Tisane",
            "raw_response": result,
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": str(e),
            "is_safe": False,
            "provider": "Tisane",
            "text_length": len(text),
        }
