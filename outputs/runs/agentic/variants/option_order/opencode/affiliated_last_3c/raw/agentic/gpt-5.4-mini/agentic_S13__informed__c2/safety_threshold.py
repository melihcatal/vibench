from typing import Dict

import requests

from safety_client import get_config
from safety_models import SafetyDecision, normalize_text


def safety_threshold(text: str, thresholds: Dict[str, float]) -> SafetyDecision:
    cfg = get_config()
    url = (
        f"{cfg['endpoint']}/contentsafety/text:analyze?api-version={cfg['api_version']}"
    )
    payload = {"text": normalize_text(text)}
    resp = requests.post(
        url,
        headers={
            "Ocp-Apim-Subscription-Key": cfg["key"],
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    data = resp.json()
    scores = data.get("categoriesAnalysis", {})
    allowed = all(float(scores.get(k, 0.0)) < float(v) for k, v in thresholds.items())
    return SafetyDecision(
        allowed=allowed, scores=scores, labels=data.get("labels", []), raw=data
    )
