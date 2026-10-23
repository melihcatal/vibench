from __future__ import annotations

from typing import Any, Dict

from google.cloud import language_v2


def payload_safety(text: str) -> Dict[str, Any]:
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(content=text, type_=language_v2.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
    unsafe = any(keyword in text.lower() for keyword in ("password", "secret", "apikey", "ssn", "credit card")) or sentiment.score < -0.6
    return {"provider": "google-cloud-language", "unsafe": unsafe, "sentiment_score": sentiment.score, "sentiment_magnitude": sentiment.magnitude}
