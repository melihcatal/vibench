from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any, Dict, Iterable, List, Optional

import requests

from safety_models import (
    AudioBriefRequest,
    BatchModerationRequest,
    EmbeddingRequest,
    ModerationRequest,
    ModerationResult,
    RedactionSpan,
    SafetyCategoryScore,
    SafetyDecision,
    TranslationRequest,
    normalize_categories,
    normalize_text,
)

PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


class SafetyClient:
    def __init__(self, api_key: Optional[str] = None, endpoint: str = PERSPECTIVE_API_ENDPOINT) -> None:
        self.api_key = api_key or os.getenv("PERSPECTIVE_API_KEY", "")
        self.endpoint = endpoint

    def _request(self, text: str, requested_attributes: Optional[Iterable[str]] = None) -> Dict[str, Any]:
        attributes = {name: {} for name in (requested_attributes or ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "THREAT", "PROFANITY"])}
        params = {"key": self.api_key}
        body = {"comment": {"text": text}, "requestedAttributes": attributes, "doNotStore": True}
        response = requests.post(self.endpoint, params=params, json=body, timeout=20)
        response.raise_for_status()
        return response.json()

    def moderate(self, request: ModerationRequest) -> ModerationResult:
        payload = self._request(normalize_text(request.text))
        scores = payload.get("attributeScores", {})
        categories = [
            SafetyCategoryScore(category=category, score=float(data.get("summaryScore", {}).get("value", 0.0)), severity=category)
            for category, data in scores.items()
        ]
        allowed = all(score.score < 0.5 for score in categories)
        decision = SafetyDecision(allowed=allowed, categories=categories, raw=payload)
        return ModerationResult(text=request.text, decision=decision)

    def moderate_batch(self, request: BatchModerationRequest) -> List[ModerationResult]:
        return [self.moderate(item) for item in request.messages]

    def redact_unsafe(self, request: ModerationRequest) -> ModerationResult:
        result = self.moderate(request)
        text = request.text
        redacted = text
        spans: List[RedactionSpan] = []
        for category in result.decision.categories:
            if category.score >= 0.5 and category.category:
                spans.append(RedactionSpan(start=0, end=len(text), label=category.category))
                redacted = "[REDACTED]"
                break
        result.redacted_text = redacted
        result.spans = spans
        return result

    def apply_thresholds(self, request: ModerationRequest, thresholds: Dict[str, float]) -> SafetyDecision:
        payload = self._request(normalize_text(request.text), requested_attributes=thresholds.keys())
        scores = payload.get("attributeScores", {})
        categories = normalize_categories(
            (
                {"category": name, "score": scores.get(name, {}).get("summaryScore", {}).get("value", 0.0)}
                for name in thresholds
            )
        )
        allowed = all(next((c.score <= thresholds[c.category] for c in categories if c.category == name), True) for name in thresholds)
        return SafetyDecision(allowed=allowed, categories=categories, raw=payload)


class TranslationClient:
    def translate_appeal(self, request: TranslationRequest) -> Dict[str, Any]:
        return {
            "text": request.text,
            "target_language": request.target_language,
            "provider": "Perspective API",
        }


class EmbeddingClient:
    def embed_rationale(self, request: EmbeddingRequest) -> Dict[str, Any]:
        vectors = [[float(len(text)), 0.0, 1.0] for text in request.texts]
        return {"provider": "Perspective API", "embeddings": vectors}


class SpeechClient:
    def generate_brief_audio(self, request: AudioBriefRequest) -> Dict[str, Any]:
        return {"provider": "Perspective API", "voice": request.voice or "neutral", "text": request.text, "audio": None}
