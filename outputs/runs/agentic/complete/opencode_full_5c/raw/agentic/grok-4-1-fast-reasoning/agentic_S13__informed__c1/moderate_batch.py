import os
import requests
import json
from typing import List
from safety_models import SafetyResult, CategoryScore
from safety_client import compute_rationale


def moderate_batch(messages: List[str]) -> List[SafetyResult]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
        "SEXUALLY_EXPLICIT": {},
    }
    results = []
    for text in messages:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": attributes,
            "languages": ["en"],
        }
        resp = requests.post(url, params={"key": api_key}, json=payload)
        resp.raise_for_status()
        data = resp.json()
        scores = []
        for cat in attributes:
            score_value = data["attributeScores"][cat]["summaryScore"]["value"]
            scores.append(CategoryScore(cat.lower(), score_value))
        blocked = any(s.severity > 0.7 for s in scores)
        rationale = compute_rationale(scores, blocked)
        results.append(
            SafetyResult(
                original_text=text,
                category_scores=scores,
                blocked=blocked,
                rationale=rationale,
            )
        )
    return results
