from typing import Dict, List, Optional
from google.cloud import language_v1
import os


def summarize_translation_quality(
    source_texts: List[str], translated_texts: List[str], target_language: str
) -> Dict[str, float]:
    """Summarize translation quality issues using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable must be set")

    sentiment_scores = []
    for source, translated in zip(source_texts, translated_texts):
        source_document = language_v1.Document(
            content=source, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        translated_document = language_v1.Document(
            content=translated, type_=language_v1.Document.Type.PLAIN_TEXT
        )

        source_sentiment = client.analyze_sentiment(
            request={"document": source_document}
        ).document_sentiment.score
        translated_sentiment = client.analyze_sentiment(
            request={"document": translated_document}
        ).document_sentiment.score

        sentiment_scores.append(abs(source_sentiment - translated_sentiment))

    avg_sentiment_diff = sum(sentiment_scores) / len(sentiment_scores)
    return {
        "average_sentiment_difference": avg_sentiment_diff,
        "quality_score": max(0, 1 - avg_sentiment_diff),
    }
