import requests
import os
import json

def vendor_text_safety(text: str) -> dict:
    if not text:
        return {"safe": True, "scores": {}}
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        return {"error": "Missing PERSPECTIVE_API_KEY"}
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text[:2000]},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "SEXUALLY_EXPLICIT": {},
            "THREAT": {}
        },
        "languages": ["en"]
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        scores = {
            attr: result['attributeScores'][attr]['summaryScore']['value']
            for attr in payload['requestedAttributes']
        }
        is_safe = all(score < 0.3 for score in scores.values())
        return {
            "safe": is_safe,
            "risky_attributes": [k for k, v in scores.items() if v >= 0.3],
            "scores": scores
        }
    except Exception as e:
        return {"error": str(e)}