import os
import requests
from typing import Dict, Any


def check_record_safety(record: Dict[str, Any]) -> Dict[str, Any]:
    text = record.get("data", {}).get("content", "")
    if not text:
        return {"safe": True, "scores": {}}
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required.")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    analysis = response.json()
    scores = {
        attr: analysis["attributeScores"][attr]["summaryScore"]["value"]
        for attr in payload["requestedAttributes"]
    }
    is_safe = all(score < 0.7 for score in scores.values())
    return {
        "safe": is_safe,
        "scores": scores,
        "analyzed_text": text[:100] + "..." if len(text) > 100 else text,
    }
