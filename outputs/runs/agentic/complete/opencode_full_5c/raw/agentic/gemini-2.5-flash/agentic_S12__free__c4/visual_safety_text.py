from google.cloud import language_v1
import os


def check_text_safety(text_content):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text_content, type=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_sentiment(request={"document": document})

    # This is a simplification. For full safety, use a dedicated moderation API.
    # Here we are using sentiment as a proxy, but a real safety check would be more robust.
    sentiment_score = response.document_sentiment.score
    sentiment_magnitude = response.document_sentiment.magnitude

    if sentiment_score < -0.5 and sentiment_magnitude > 1:
        return {
            "safety_status": "potentially unsafe",
            "sentiment_score": sentiment_score,
            "sentiment_magnitude": sentiment_magnitude,
        }
    else:
        return {
            "safety_status": "likely safe",
            "sentiment_score": sentiment_score,
            "sentiment_magnitude": sentiment_magnitude,
        }
