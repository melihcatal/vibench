from google.cloud import language_v1 as language
from speech_models import TranscriptionResult


def archive_summary(transcript: TranscriptionResult) -> str:
    """Summarize transcription results using Google Cloud Natural Language API."""
    client = language.LanguageServiceClient()
    full_text = " ".join([segment.text for segment in transcript.segments])

    document = language.Document(
        content=full_text,
        type_=language.Document.Type.PLAIN_TEXT,
    )
    response = client.analyze_entities(request={"document": document})

    summary = "Key entities discussed:\n"
    for entity in response.entities:
        summary += (
            f"- {entity.name} ({entity.type_.name}): {entity.salience:.2%} relevance\n"
        )

    return summary
