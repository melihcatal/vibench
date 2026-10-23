import os
from google.cloud import language_v1


def moderate_transcript_text(transcript_text):
    """Moderate transcript text before publishing using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=transcript_text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
    )

    response = client.moderate_text(document=document)

    moderation_categories = []

    for category in response.moderation_categories:
        moderation_categories.append(
            {
                "name": category.name,
                "confidence": category.confidence,
                "thresholded": category.confidence > 0.5,
            }
        )

    return {
        "original_text": transcript_text,
        "moderation_categories": moderation_categories,
        "has_content_warnings": any(
            cat["thresholded"] for cat in moderation_categories
        ),
    }
