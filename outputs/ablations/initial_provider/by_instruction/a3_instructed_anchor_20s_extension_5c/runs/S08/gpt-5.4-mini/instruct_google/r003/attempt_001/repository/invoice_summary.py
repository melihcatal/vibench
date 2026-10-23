from typing import Any, Dict

from google.cloud import language_v1


def invoice_summary(fields: Dict[str, Any]) -> Dict[str, Any]:
    client = language_v1.LanguageServiceClient()
    text = f"Invoice from {fields.get('vendor') or fields.get('party')}, total {fields.get('total') or fields.get('amount')}"
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
    return {"summary": text, "sentiment_score": float(sentiment.score), "sentiment_magnitude": float(sentiment.magnitude)}
