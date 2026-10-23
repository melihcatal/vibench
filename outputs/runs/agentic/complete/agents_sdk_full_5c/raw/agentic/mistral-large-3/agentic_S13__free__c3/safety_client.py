import os
from typing import List, Dict, Optional
import requests
from safety_models import (
    SafetyCategory,
    TextModerationRequest,
    BatchModerationRequest,
    ModerationDecision,
    SafetySpan,
    normalize_category,
    normalize_severity,
)


class GoogleContentSafetyClient:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_CONTENT_SAFETY_API_KEY")
        self.base_url = "https://contentmoderator.googleapis.com/v1/projects/-/locations/global"
        if not self.api_key:
            raise ValueError("GOOGLE_CONTENT_SAFETY_API_KEY environment variable not set")

    def _build_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def moderate_text(self, request: TextModerationRequest) -> ModerationDecision:
        url = f"{self.base_url}:analyzeText"
        payload = {
            "text": request["text"],
            "categories": [c.value for c in request.get("categories", list(SafetyCategory))],
        }
        response = requests.post(url, headers=self._build_headers(), json=payload)
        response.raise_for_status()
        return self._parse_response(response.json())

    def moderate_batch(self, request: BatchModerationRequest) -> List[ModerationDecision]:
        url = f"{self.base_url}:batchAnalyzeText"
        payload = {
            "requests": [
                {
                    "text": text,
                    "categories": [c.value for c in request.get("categories", list(SafetyCategory))],
                }
                for text in request["texts"]
            ]
        }
        response = requests.post(url, headers=self._build_headers(), json=payload)
        response.raise_for_status()
        return [self._parse_response(r) for r in response.json().get("responses", [])]

    def _parse_response(self, response: Dict) -> ModerationDecision:
        categories = {}
        scores = {}
        spans = []

        for category_result in response.get("moderationCategories", []):
            category = normalize_category(category_result["name"])
            score = category_result["confidence"]
            blocked = category_result.get("blocked", False)
            categories[category] = blocked
            scores[category] = score

        for span_result in response.get("spans", []):
            for category_result in span_result.get("moderationCategories", []):
                span = SafetySpan(
                    start=span_result["start"],
                    end=span_result["end"],
                    category=normalize_category(category_result["name"]),
                    severity=normalize_severity(category_result.get("severity", "none")),
                    confidence=category_result["confidence"],
                )
                spans.append(span)

        allowed = not any(categories.values())
        return ModerationDecision(
            allowed=allowed, categories=categories, scores=scores, spans=spans
        )