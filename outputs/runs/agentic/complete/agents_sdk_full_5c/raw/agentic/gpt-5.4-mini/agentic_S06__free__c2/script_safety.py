from __future__ import annotations

from google.cloud import language_v1


NEGATIVE = {"hate", "violence", "kill", "attack", "self-harm"}


def check_script_safety(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
    unsafe_terms = sorted({term for term in NEGATIVE if term in text.lower()})
    return {
        "unsafe_terms": unsafe_terms,
        "score": float(getattr(sentiment, "score", 0.0)),
        "magnitude": float(getattr(sentiment, "magnitude", 0.0)),
        "is_safe": not unsafe_terms and float(getattr(sentiment, "score", 0.0)) > -0.7,
    }
