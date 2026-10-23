from typing import Any, Dict, List

import requests

from safety_client import get_config
from safety_models import SafetyDecision, normalize_text


def moderate_batch(messages: List[str]) -> List[SafetyDecision]:
    cfg = get_config()
    url = (
        f"{cfg['endpoint']}/contentsafety/text:analyze?api-version={cfg['api_version']}"
    )
    results: List[SafetyDecision] = []
    for message in messages:
        payload: Dict[str, Any] = {"text": normalize_text(message)}
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
        results.append(
            SafetyDecision(
                allowed=not data.get("blocklistMatched", False),
                scores=data.get("categoriesAnalysis", {}),
                labels=data.get("labels", []),
                raw=data,
            )
        )
    return results
