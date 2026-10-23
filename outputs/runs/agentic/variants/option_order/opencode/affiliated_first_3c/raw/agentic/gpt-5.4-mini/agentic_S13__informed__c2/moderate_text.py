import requests

from safety_client import auth_headers, endpoint_url, has_safety_credentials
from safety_models import ModerationRequest, decision_from_scores, normalize_text


def moderate_text(text: str, threshold: float = 0.5):
    payload = {
        "text": normalize_text(text),
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
    }
    if has_safety_credentials():
        response = requests.post(
            endpoint_url("/contentsafety/text:analyze"),
            json=payload,
            headers=auth_headers(),
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        scores = {
            item["category"]: float(item["severity"] or item.get("score", 0.0))
            for item in data.get("categoriesAnalysis", [])
        }
        return decision_from_scores(scores, threshold)
    scores = {"Hate": 0.0, "SelfHarm": 0.0, "Sexual": 0.0, "Violence": 0.0}
    return decision_from_scores(scores, threshold)
