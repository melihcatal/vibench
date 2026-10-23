import os
import requests
import json

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_prompt_safety(text: str) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        return {"safe": True, "reason": "PERSPECTIVE_API_KEY not set"}
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }
    try:
        response = requests.post(
            f"{PERSPECTIVE_API_URL}?key={api_key}",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        result = response.json()
        scores = {
            attr: result["attributeScores"][attr]["summaryScore"]["value"]
            for attr in result["attributeScores"]
        }
        is_safe = all(scores[attr] < 0.5 for attr in scores)
        return {"safe": is_safe, "scores": scores}
    except Exception:
        return {"safe": True, "error": "API call failed"}
