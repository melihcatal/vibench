from google.cloud import language_v1 as language
from speech_models import TranscriptionResult
import os


def moderate_transcript(transcript: TranscriptionResult) -> dict:
    client = language.LanguageServiceClient()

    results = {}
    for segment in transcript.segments:
        document = language.Document(
            content=segment.text, type_=language.Document.Type.PLAIN_TEXT
        )

        response = client.analyze_sentiment(request={"document": document})

        response_moderation = client.moderate_text(request={"document": document})

        results[segment.text] = {
            "sentiment": {
                "score": response.document_sentiment.score,
                "magnitude": response.document_sentiment.magnitude,
            },
            "moderation_categories": [
                {"name": category.name, "confidence": category.confidence}
                for category in response_moderation.moderation_categories
            ],
        }

    return results
