from __future__ import annotations

from dataclasses import dataclass

from google.cloud import language_v1


@dataclass
class SafetyResult:
    safe: bool
    score: float
    reason: str


def payload_safety(text: str) -> SafetyResult:
    client = language_v1.LanguageServiceClient()
    doc = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": doc}).document_sentiment
    score = float(sentiment.score) if sentiment else 0.0
    safe = score >= -0.25 and not any(term in text.lower() for term in ("secret", "password", "ssn"))
    reason = "content appears safe" if safe else "content may be sensitive or unsafe"
    return SafetyResult(safe=safe, score=score, reason=reason)
