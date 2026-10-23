from __future__ import annotations

from typing import Iterable

import requests

from speech_models import SafetyResult, normalize_text


class LiveCaptionSafetyChecker:
    def __init__(self, endpoint: str, key: str) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.key = key

    def check_text(self, text: str) -> SafetyResult:
        text = normalize_text(text)
        url = f"{self.endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
        payload = {"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}
        headers = {"Ocp-Apim-Subscription-Key": self.key, "Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        categories = {item.get("category", "unknown"): float(item.get("severity", 0)) for item in data.get("categoriesAnalysis", [])}
        flagged = any(sev >= 2 for sev in categories.values())
        return SafetyResult(text=text, flagged=flagged, categories=categories, raw=data)

    def check_stream(self, chunks: Iterable[str]) -> Iterable[SafetyResult]:
        for chunk in chunks:
            yield self.check_text(chunk)
