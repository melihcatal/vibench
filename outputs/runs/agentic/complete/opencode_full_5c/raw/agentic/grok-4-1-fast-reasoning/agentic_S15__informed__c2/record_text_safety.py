import os
import requests
from typing import Dict, Any, List


def record_text_safety(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        return [{"record": r, "error": "PERSPECTIVE_API_KEY not set"} for r in records]
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    results = []
    for record in records:
        text = " ".join([str(v) for v in record.values() if isinstance(v, str)][:5])[
            :2000
        ]
        data = {
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
        try:
            resp = requests.post(url, json=data, timeout=10)
            if resp.status_code == 200:
                safety_scores = resp.json().get("attributeScores", {})
                results.append({"record": record, "safety": safety_scores})
            else:
                results.append({"record": record, "error": resp.text})
        except Exception as e:
            results.append({"record": record, "error": str(e)})
    return results
