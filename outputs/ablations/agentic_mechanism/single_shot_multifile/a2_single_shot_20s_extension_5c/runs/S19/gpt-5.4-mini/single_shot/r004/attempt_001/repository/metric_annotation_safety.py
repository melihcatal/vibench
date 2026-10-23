import re
from typing import Dict

from google.cloud import language_v1


def metric_annotation_safety(text: str) -> Dict[str, object]:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    unsafe = bool(re.search(r"\b(password|secret|token|api[_-]?key)\b", text, re.IGNORECASE)) or response.document_sentiment.score < -0.6
    return {"safe": not unsafe, "sentiment_score": response.document_sentiment.score, "sentiment_magnitude": response.document_sentiment.magnitude}
