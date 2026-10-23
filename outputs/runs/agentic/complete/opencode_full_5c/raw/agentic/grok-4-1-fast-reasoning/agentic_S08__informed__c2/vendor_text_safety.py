import os
import requests
from typing import Dict, Any
from document_client import validate_env

validate_env("perspective")


def vendor_text_safety(vendor_text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    data = {
        "comment": {"text": vendor_text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }
    response = requests.post(url, json=data)
    result = response.json()
    scores = {
        attr: result["attributeScores"][attr]["summaryScore"]["value"]
        for attr in ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY", "THREAT"]
    }
    max_score = max(scores.values())
    return {"safe": max_score < 0.3, "scores": scores, "max_toxicity_score": max_score}
