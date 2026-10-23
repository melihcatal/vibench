import os
from google.cloud import language_v1 as language
from speech_models import TranscriptionResult

def moderate_transcript(transcript: str) -> dict:
    """Moderate transcript text before publishing using Google Cloud Natural Language API."""
    client = language.LanguageServiceClient()
    document = language.Document(
        content=transcript, type_=language.Document.Type.PLAIN_TEXT
    )

    response = client.moderate_text(document=document)

    return {
        "moderation_scores": {
            "toxicity": response.moderation_config.score,
            "categories": [
                {"name": category.name, "confidence": category.confidence}
                for category in response.moderation_categories
            ],
        }
    }