from google.cloud import language_v1 as language
import os


def script_safety(text: str) -> dict:
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})

    sentiment = response.document_sentiment
    safety_score = 1.0 - max(0, sentiment.score)

    return {
        "safety_score": safety_score,
        "is_safe": safety_score < 0.7,
        "sentiment": {"score": sentiment.score, "magnitude": sentiment.magnitude},
    }
