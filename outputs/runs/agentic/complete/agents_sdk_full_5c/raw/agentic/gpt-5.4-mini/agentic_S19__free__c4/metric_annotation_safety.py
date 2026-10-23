from __future__ import annotations

from google.cloud import language_v1

from observability_client import load_config
from observability_models import SafetyCheckResult


def metric_annotation_safety(text: str) -> dict:
    load_config()
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document, "encoding_type": language_v1.EncodingType.UTF8})
    score = response.document_sentiment.score if response.document_sentiment else 0.0
    safe = abs(score) < 0.6 and len(text) < 500
    result = SafetyCheckResult(content=text, safe=safe, reason="sentiment_and_length_check")
    return {**result.__dict__, "sentiment_score": score}
