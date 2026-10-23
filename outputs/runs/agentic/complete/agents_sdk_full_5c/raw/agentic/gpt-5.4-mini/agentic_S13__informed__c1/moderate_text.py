from typing import Dict

import requests

from safety_client import build_client, clean_input
from safety_models import ModerationDecision, ModerationRequest

PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = "PERSPECTIVE_API_KEY"


def moderate_text(request: ModerationRequest) -> ModerationDecision:
    text = clean_input(request.text)
    client = build_client()
    payload: Dict[str, object] = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        "languages": [request.language] if request.language else None,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.post(
        f"{PERSPECTIVE_API_HOST}?key={PERSPECTIVE_API_KEY}",
        json=payload,
        timeout=client.timeout,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        attr.lower(): data["attributeScores"][attr]["summaryScore"]["value"]
        for attr in data.get("attributeScores", {})
    }
    allowed = all(score < 0.5 for score in scores.values())
    reasons = [f"{k}={v:.3f}" for k, v in scores.items() if v >= 0.5]
    return ModerationDecision(allowed=allowed, category_scores=scores, reasons=reasons)
