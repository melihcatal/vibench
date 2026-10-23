from __future__ import annotations

from google.cloud import language_v1

from messaging_models import SafetyCheckResult


def check_message_safety(text: str) -> SafetyCheckResult:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    score = response.document_sentiment.score if response.document_sentiment else 0.0
    safe = score >= -0.2
    return SafetyCheckResult(safe=safe, reason=f"google-cloud-language sentiment={score:.2f}")
