from typing import Dict

from google.cloud import language_v1


_BAD_TERMS = {"abuse", "fraud", "scam", "malware", "phishing"}


def check_message_payload_text(text: str) -> Dict[str, object]:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
    unsafe = any(term in text.lower() for term in _BAD_TERMS)
    return {"provider": "google-cloud-language", "unsafe": unsafe, "score": float(sentiment.score) if sentiment else 0.0, "magnitude": float(sentiment.magnitude) if sentiment else 0.0}
