from google.cloud import language_v1
import os


def moderate_vendor_text(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Analyze sentiment to detect potentially negative or aggressive language
    sentiment_response = client.analyze_sentiment(document=document)
    sentiment_score = sentiment_response.document_sentiment.score
    sentiment_magnitude = sentiment_response.document_sentiment.magnitude

    # Classify text to detect sensitive categories
    classification_response = client.classify_text(document=document)
    categories = [category.name for category in classification_response.categories]

    safety_status = "SAFE"
    reasons = []

    if (
        sentiment_score < -0.5 and sentiment_magnitude > 1.0
    ):  # Strongly negative sentiment
        safety_status = "UNSAFE"
        reasons.append("Strongly negative sentiment detected.")

    # Example: Check for specific categories that might indicate unsafe content
    for category in categories:
        if (
            "/Adult" in category
            or "/Violence" in category
            or "/Illicit Activities" in category
        ):
            safety_status = "UNSAFE"
            reasons.append(f"Content categorized as: {category}")

    return {
        "text": text,
        "safety_status": safety_status,
        "sentiment_score": sentiment_score,
        "sentiment_magnitude": sentiment_magnitude,
        "categories": categories,
        "reasons": reasons,
    }
