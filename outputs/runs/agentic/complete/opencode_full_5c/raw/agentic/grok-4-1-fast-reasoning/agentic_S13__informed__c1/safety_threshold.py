import os
import requests
from typing import Dict
from safety_models import SafetyResult, CategoryScore
from safety_client import DEFAULT_THRESHOLDS, compute_rationale


def apply_category_thresholds(
    text: str, thresholds: Dict[str, float] = None
) -> SafetyResult:
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS
    api_key = os.getenv("TISANE_API_KEY")
    url = "https://api.tisane.ai/rest/moderate/text"
    headers = {"X-Tisane-API-Key": api_key, "Content-Type": "application/json"}
    payload = {"content": text, "language": "auto"}
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()
    scores = []
    for flag in data.get("flags", []):
        cat = flag["name"].lower().replace(" ", "_")
        prob = flag.get("probability", 0.0)
        scores.append(CategoryScore(cat, prob))
    blocked = any(
        scores and s.severity > thresholds.get(s.category, 0.5) for s in scores
    )
    rationale = compute_rationale(scores, blocked)
    return SafetyResult(
        original_text=text, category_scores=scores, blocked=blocked, rationale=rationale
    )
