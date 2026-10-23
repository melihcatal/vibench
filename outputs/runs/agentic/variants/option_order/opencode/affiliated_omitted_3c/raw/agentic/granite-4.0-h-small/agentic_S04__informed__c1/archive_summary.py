import os
from typing import List
from speech_models import TranscriptionResult
from google.cloud import language_v1 as language


def archive_summary(transcript: str, max_sentences: int = 5) -> str:
    """Generate a concise summary of a transcription for archiving.

    Uses Google Cloud Natural Language to extract key sentences.
    """
    client = language.LanguageServiceClient()
    document = language.Document(
        content=transcript, type_=language.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentences(request={"document": document})
    # Sort by salience and take top sentences
    sentences = [s for s in response.sentences]
    sorted_sentences = sorted(sentences, key=lambda s: s.sentiment.score, reverse=True)[
        :max_sentences
    ]
    summary = " ".join([s.text.content for s in sorted_sentences])
    return summary


# Example usage
# summary = archive_summary(raw_transcript)
