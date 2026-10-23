import requests
from typing import List
from safety_client import get_api_key
from safety_models import ModerationResult, normalize_categories

ATTRIBUTES = {
    "TOXICITY": {},
    "SEVERE_TOXICITY": {},
    "IDENTITY_ATTACK": {},
    "INSULT": {},
    "PROFANITY": {},
    "THREAT": {},
    "SEXUALLY_EXPLICIT": {},
}


def moderate_batch(texts: List[str]) -> List[ModerationResult]:
    key = get_api_key("perspective")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={key}"
    results = []
    for text in texts:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": ATTRIBUTES,
            "languages": ["en"],
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        raw_scores = {}
        for attr, score_data in data["attributeScores"].items():
            raw_scores[attr.lower()] = score_data["summaryScore"]["default"]["score"][
                "value"
            ]
        scores = normalize_categories(raw_scores)
        flagged = any(score.probability > 0.5 for score in scores)
        results.append(
            ModerationResult(input_text=text, scores=scores, flagged=flagged)
        )
    return results
