from google.cloud import language_v1 as language
from speech_models import TranscriptionResult, TranscriptSegment
from typing import Dict


def archive_summary(transcript: TranscriptionResult) -> Dict[str, str]:
    """
    Summarizes transcription results using Google Cloud Natural Language API.

    Args:
        transcript: TranscriptionResult containing segments to summarize.

    Returns:
        Dictionary containing summary and key insights.
    """
    client = language.LanguageServiceClient()
    document = language.Document(
        content=" ".join([segment.text for segment in transcript.segments]),
        type_=language.Document.Type.PLAIN_TEXT,
    )

    response = client.analyze_entities(request={"document": document})
    entities = [
        {
            "name": entity.name,
            "type": language.Entity.Type(entity.type_).name,
            "salience": entity.salience,
        }
        for entity in response.entities
    ]

    summary_response = client.analyze_sentiment(request={"document": document})
    sentiment = {
        "score": summary_response.document_sentiment.score,
        "magnitude": summary_response.document_sentiment.magnitude,
    }

    return {
        "summary": " ".join([segment.text for segment in transcript.segments[:3]])
        + "...",
        "key_entities": str(entities),
        "sentiment": str(sentiment),
    }
