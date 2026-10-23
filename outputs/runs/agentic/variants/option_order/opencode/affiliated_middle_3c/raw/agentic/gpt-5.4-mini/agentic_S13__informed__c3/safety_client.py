import os
from typing import Any, Dict, Optional

import requests

from safety_models import (
    BatchModerationRequest,
    BatchModerationResult,
    ModerationResult,
    RedactionResult,
    TextModerationRequest,
    ThresholdDecision,
    ThresholdRule,
    normalize_categories,
    normalize_category_scores,
)

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


class SafetyClient:
    def __init__(self, api_key: Optional[str] = None, timeout: float = 30.0):
        self.api_key = api_key or os.environ.get("PERSPECTIVE_API_KEY")
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        return {"Content-Type": "application/json"}

    def _params(self) -> Dict[str, str]:
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY is required")
        return {"key": self.api_key}

    def moderate_text(self, request: TextModerationRequest) -> ModerationResult:
        payload = {
            "comment": {"text": request.text},
            "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "IDENTITY_ATTACK": {}, "INSULT": {}, "THREAT": {}, "SEXUALLY_EXPLICIT": {}, "FLIRTATION": {}, "PROFANITY": {}},
            "doNotStore": True,
        }
        if request.language:
            payload["languages"] = [request.language]
        response = requests.post(PERSPECTIVE_API_URL, params=self._params(), headers=self._headers(), json=payload, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        scores = {k.lower(): v["summaryScore"]["value"] for k, v in data.get("attributeScores", {}).items() if "summaryScore" in v}
        categories = {k.lower(): v >= 0.5 for k, v in scores.items()}
        return ModerationResult(flagged=any(categories.values()), category_scores=normalize_category_scores(scores), categories=normalize_categories(categories), raw=data)

    def moderate_batch(self, request: BatchModerationRequest):
        results = [self.moderate_text(TextModerationRequest(text=msg, language=request.language)) for msg in request.messages]
        return BatchModerationResult(results=results, raw={"count": len(results)})

    def redact_unsafe(self, text: str, threshold: float = 0.5) -> RedactionResult:
        result = self.moderate_text(TextModerationRequest(text=text))
        spans = []
        redacted_text = text
        if result.flagged:
            redacted_text = "[REDACTED]" if max(result.category_scores.values() or [0.0]) >= threshold else text
            if redacted_text != text:
                spans.append({"start": 0, "end": len(text), "category": max(result.category_scores, key=result.category_scores.get, default="unknown")})
        return RedactionResult(redacted_text=redacted_text, spans=spans, raw=result.raw)

    def safety_threshold(self, text: str, rules: Dict[str, float]) -> ThresholdDecision:
        result = self.moderate_text(TextModerationRequest(text=text))
        triggered = [cat for cat, th in rules.items() if result.category_scores.get(cat.lower(), 0.0) >= th]
        return ThresholdDecision(allowed=not triggered, triggered_categories=triggered, raw=result.raw)
