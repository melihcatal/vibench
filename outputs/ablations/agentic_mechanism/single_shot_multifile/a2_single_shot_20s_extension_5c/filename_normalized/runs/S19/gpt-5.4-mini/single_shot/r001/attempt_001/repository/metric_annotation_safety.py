from __future__ import annotations

import re
from typing import Dict

from google.cloud import language_v1


def metric_annotation_safety(text: str) -> Dict[str, object]:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
    unsafe = bool(re.search(r"\b(password|secret|token|apikey|api key|credential)\b", text, re.IGNORECASE)) or (sentiment.score < -0.5 if sentiment else False)
    return {
        "safe": not unsafe,
        "reason": "contains sensitive terms or strongly negative tone" if unsafe else "ok",
        "sentiment_score": sentiment.score if sentiment else None,
        "sentiment_magnitude": sentiment.magnitude if sentiment else None,
    }
