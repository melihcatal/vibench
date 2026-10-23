from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

from safety_models import TextSafetyDecision, TextSafetyRequest, normalize_text


@dataclass
class SafetyClientConfig:
    endpoint: str
    api_key: str
    service: str = "Azure AI Content Safety"


class SafetyClient:
    def __init__(self, config: Optional[SafetyClientConfig] = None) -> None:
        endpoint = (config.endpoint if config else os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "")).rstrip("/")
        api_key = config.api_key if config else os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
        self.config = SafetyClientConfig(endpoint=endpoint, api_key=api_key)

    def analyze_text(self, request: TextSafetyRequest) -> TextSafetyDecision:
        text = normalize_text(request.text)
        url = f"{self.config.endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview"
        headers = {
            "Ocp-Apim-Subscription-Key": self.config.api_key,
            "Content-Type": "application/json",
        }
        payload: Dict[str, Any] = {
            "text": text,
            "categories": request.categories,
            "language": request.language,
        }
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        raw = response.json()
        scores = {item.get("category", ""): float(item.get("severity", 0.0)) for item in raw.get("categoriesAnalysis", [])}
        labels = {category: score >= 0.5 for category, score in scores.items()}
        allowed = not any(labels.values())
        return TextSafetyDecision(allowed=allowed, scores=scores, labels=labels, provider=self.config.service, raw=raw)
