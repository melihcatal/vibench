import os
from typing import Any, Dict

import requests

from safety_client import get_config
from safety_models import (
    SafetyDecision,
    SafetyRequest,
    normalize_categories,
    normalize_text,
)


def moderate_text(text: str, categories=None, locale=None) -> SafetyDecision:
    req = SafetyRequest(
        text=normalize_text(text),
        categories=normalize_categories(categories),
        locale=locale,
    )
    cfg = get_config()
    url = (
        f"{cfg['endpoint']}/contentsafety/text:analyze?api-version={cfg['api_version']}"
    )
    payload: Dict[str, Any] = {"text": req.text}
    if req.categories:
        payload["categories"] = req.categories
    if req.locale:
        payload["language"] = req.locale
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
    return SafetyDecision(
        allowed=not data.get("blocklistMatched", False),
        scores=data.get("categoriesAnalysis", {}),
        labels=data.get("labels", []),
        raw=data,
    )
