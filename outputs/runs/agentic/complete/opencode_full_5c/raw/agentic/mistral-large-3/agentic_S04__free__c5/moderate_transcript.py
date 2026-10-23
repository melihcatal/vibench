from google.cloud import language_v1 as language
from speech_models import TranscriptionResult


def moderate_transcript(transcript: TranscriptionResult) -> dict:
    """Moderate transcript text using Google Cloud Natural Language API."""
    client = language.LanguageServiceClient()
    results = {}

    for segment in transcript.segments:
        document = language.Document(
            content=segment.text,
            type_=language.Document.Type.PLAIN_TEXT,
        )
        response = client.analyze_sentiment(request={"document": document})

        results[segment.text] = {
            "sentiment_score": response.document_sentiment.score,
            "sentiment_magnitude": response.document_sentiment.magnitude,
            "moderation_suggested": response.document_sentiment.score < -0.5,
        }

    return results
