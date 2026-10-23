from typing import List, Dict
import os
from google.cloud import language_v1


def summarize_translation_quality(
    source_texts: List[str], translated_texts: List[str]
) -> Dict[str, float]:
    """
    Summarizes translation quality issues using Google Cloud Natural Language API.
    Returns a dictionary with quality metrics.
    """
    client = language_v1.LanguageServiceClient()

    if not os.getenv("GOOGLE_CLOUD_PROJECT_ID"):
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable must be set")

    sentiment_scores = []
    entity_counts = []

    for source, translated in zip(source_texts, translated_texts):
        # Analyze source text
        source_document = language_v1.Document(
            content=source, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        source_sentiment = client.analyze_sentiment(
            request={"document": source_document}
        ).document_sentiment
        source_entities = client.analyze_entities(
            request={"document": source_document}
        ).entities

        # Analyze translated text
        translated_document = language_v1.Document(
            content=translated, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        translated_sentiment = client.analyze_sentiment(
            request={"document": translated_document}
        ).document_sentiment
        translated_entities = client.analyze_entities(
            request={"document": translated_document}
        ).entities

        # Calculate sentiment difference
        sentiment_diff = abs(source_sentiment.score - translated_sentiment.score)
        sentiment_scores.append(sentiment_diff)

        # Calculate entity count difference
        entity_diff = abs(len(source_entities) - len(translated_entities))
        entity_counts.append(entity_diff)

    avg_sentiment_diff = (
        sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
    )
    avg_entity_diff = sum(entity_counts) / len(entity_counts) if entity_counts else 0

    return {
        "avg_sentiment_difference": avg_sentiment_diff,
        "avg_entity_difference": avg_entity_diff,
        "quality_score": max(0, 1 - (avg_sentiment_diff + avg_entity_diff / 10)),
    }
