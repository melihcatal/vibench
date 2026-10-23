import os
import requests
from typing import Dict, Any
from identity_models import UserProfile


def moderate_user_claims(profile: UserProfile) -> Dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    texts = []
    if profile.name:
        texts.append(profile.name)
    if profile.email:
        texts.append(profile.email)
    scores = {}
    for i, text in enumerate(texts):
        data = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
            "doNotStore": True,
        }
        resp = requests.post(url, json=data)
        resp.raise_for_status()
        result = resp.json()
        attr_scores = result.get("attributeScores", {})
        scores[f"text_{i}_toxicity"] = (
            attr_scores.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
        )
        scores[f"text_{i}_insult"] = (
            attr_scores.get("INSULT", {}).get("summaryScore", {}).get("value", 0.0)
        )
        scores[f"text_{i}_profanity"] = (
            attr_scores.get("PROFANITY", {}).get("summaryScore", {}).get("value", 0.0)
        )
    return scores


if __name__ == "__main__":
    pass
