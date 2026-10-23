from typing import Any, Dict
from google.cloud import language_v1


def check_ocr_safety(text: str) -> Dict[str, Any]:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(request={'document': document})
    return {'provider': 'google_cloud_language_v1', 'score': annotations.document_sentiment.score, 'magnitude': annotations.document_sentiment.magnitude}
