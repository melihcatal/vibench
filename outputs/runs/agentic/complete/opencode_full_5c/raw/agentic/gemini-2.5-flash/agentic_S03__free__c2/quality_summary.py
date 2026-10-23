from google.cloud import language_v1
from translation_models import QualitySummaryRequest, QualitySummaryResponse
import os


def summarize_quality_issues(request: QualitySummaryRequest) -> QualitySummaryResponse:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=request.text,
        type=language_v1.Document.Type.PLAIN_TEXT,
        language=request.language,
    )

    # Perform sentiment analysis
    sentiment_response = client.analyze_sentiment(request={"document": document})
    sentiment = sentiment_response.document_sentiment

    # Perform entity analysis
    entity_response = client.analyze_entities(request={"document": document})
    entities = entity_response.entities

    summary = f"Sentiment Score: {sentiment.score}, Magnitude: {sentiment.magnitude}. "
    summary += (
        "Entities found: " + ", ".join([entity.name for entity in entities]) + "."
    )

    # Simple logic for quality summary based on sentiment (can be expanded)
    if sentiment.score < -0.2:  # Example threshold for negative sentiment
        summary += " Potential quality issues detected due to negative sentiment."
    elif (
        sentiment.magnitude > 1.0 and sentiment.score < 0.2
    ):  # High magnitude with neutral-ish score might indicate complex or conflicting emotions
        summary += " Text is emotionally charged, review for nuances."
    else:
        summary += " Text appears to have neutral or positive sentiment."

    return QualitySummaryResponse(summary=summary)


# Provider-identifying signal: google.cloud.language_v1 import
