import requests
from safety_client import get_perspective_api_key
from safety_models import ModerationResult

PERSPECTIVE_ANALYZE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def is_text_allowed(text: str, category_thresholds: dict[str, float] | None = None) -> bool:
    if category_thresholds is None:
        category_thresholds = {
            "TOXICITY": 0.5,
            "SEVERE_TOXICITY": 0.5,
            "INSULT": 0.5,
            "PROFANITY": 0.5,
            "THREAT": 0.5
        }
    api_key = get_perspective_api_key()
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {k: {} for k in category_thresholds}
    }
    params = {"key": api_key}
    response = requests.post(PERSPECTIVE_ANALYZE_URL, json=data, params=params)
    response.raise_for_status()
    api_response = response.json()
    attr_scores = api_response["attributeScores"]
    scores = {
        attr: attr_scores[attr]["summaryScore"]["score"]["value"]
        for attr in attr_scores
    }
    return all(scores.get(cat, 0.0) <= thresh for cat, thresh in category_thresholds.items())