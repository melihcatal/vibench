import os
from typing import List, Dict, Any
from translation_models import TranslationResponse


def summarize_translation_quality(
    original_text: str,
    translated_text: str,
    source_lang: str = "en",
    target_lang: str = "es",
) -> Dict[str, Any]:
    """
    Summarize translation quality issues using Google Cloud Natural Language API.

    Args:
        original_text: Original source text
        translated_text: Translated text
        source_lang: Source language code
        target_lang: Target language code

    Returns:
        Dictionary with quality metrics and issues
    """
    try:
        # Import Google Cloud Natural Language API
        from google.cloud import language_v1

        # Initialize client
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
            )

        client = language_v1.LanguageServiceClient()

        # Analyze sentiment of original text
        original_document = language_v1.Document(
            content=original_text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
            language=source_lang,
        )
        original_sentiment = client.analyze_sentiment(
            request={"document": original_document}
        ).document_sentiment

        # Analyze sentiment of translated text
        translated_document = language_v1.Document(
            content=translated_text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
            language=target_lang,
        )
        translated_sentiment = client.analyze_sentiment(
            request={"document": translated_document}
        ).document_sentiment

        # Calculate sentiment preservation score
        sentiment_diff = abs(original_sentiment.score - translated_sentiment.score)
        sentiment_preservation = max(0, 1 - sentiment_diff)

        # Analyze entities in original text
        original_entities = client.analyze_entities(
            request={"document": original_document}
        ).entities

        # Analyze entities in translated text
        translated_entities = client.analyze_entities(
            request={"document": translated_document}
        ).entities

        # Count named entities
        original_entity_count = len(original_entities)
        translated_entity_count = len(translated_entities)

        # Simple length ratio check
        length_ratio = len(translated_text) / max(len(original_text), 1)

        # Compile quality summary
        quality_summary = {
            "sentiment_preservation_score": round(sentiment_preservation, 3),
            "original_sentiment_score": round(original_sentiment.score, 3),
            "translated_sentiment_score": round(translated_sentiment.score, 3),
            "original_magnitude": round(original_sentiment.magnitude, 3),
            "translated_magnitude": round(translated_sentiment.magnitude, 3),
            "entity_preservation": {
                "original_count": original_entity_count,
                "translated_count": translated_entity_count,
                "ratio": round(
                    translated_entity_count / max(original_entity_count, 1), 3
                ),
            },
            "length_ratio": round(length_ratio, 3),
            "potential_issues": [],
        }

        # Identify potential issues
        if sentiment_preservation < 0.7:
            quality_summary["potential_issues"].append(
                "Sentiment may not be preserved accurately"
            )

        if length_ratio < 0.5 or length_ratio > 2.0:
            quality_summary["potential_issues"].append(
                f"Length ratio ({length_ratio:.2f}) suggests possible over/under translation"
            )

        if translated_entity_count < original_entity_count * 0.5:
            quality_summary["potential_issues"].append(
                "Significant loss of named entities"
            )

        return quality_summary

    except Exception as e:
        raise Exception(f"Quality analysis failed: {str(e)}")
