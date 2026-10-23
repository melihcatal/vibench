"""Translate live captions into another language using Google Cloud Translation API.

Translates real-time speech-to-text transcripts using the Google Cloud Translation v2 API.
"""

from typing import Optional

from google.cloud import translate_v2 as translate
from google.cloud.translate_v2 import Client as TranslateClient

from partial_results import handle_recognition_event
from speech_models import clean_transcript_text

# Google Cloud Translation API endpoint
GOOGLE_TRANSLATE_API_ENDPOINT = "translation.googleapis.com"


def get_translate_client() -> TranslateClient:
    """Create a Google Cloud Translation v2 client.

    Returns:
        Configured TranslateClient instance.
    """
    return translate.Client()


def translate_caption(
    transcript: str,
    source_language: str = "en",
    target_language: str = "es",
) -> str:
    """Translate a single caption transcript using Google Cloud Translation.

    Args:
        transcript: The source transcript text to translate.
        source_language: Source language code (ISO 639-1).
        target_language: Target language code (ISO 639-1).

    Returns:
        Translated text in the target language.
    """
    client = get_translate_client()
    cleaned = clean_transcript_text(transcript)

    if not cleaned:
        return ""

    result = client.translate(
        cleaned,
        source_language=source_language,
        target_language=target_language,
        format_="text",
    )

    return result.get("translatedText", "")


def translate_caption_batch(
    transcripts: list,
    source_language: str = "en",
    target_language: str = "es",
) -> list:
    """Translate multiple caption transcripts in a single batch request.

    Args:
        transcripts: List of source transcript strings.
        source_language: Source language code (ISO 639-1).
        target_language: Target language code (ISO 639-1).

    Returns:
        List of translated texts in the target language.
    """
    client = get_translate_client()
    cleaned_texts = [clean_transcript_text(t) for t in transcripts if t.strip()]

    if not cleaned_texts:
        return []

    results = client.translate(
        cleaned_texts,
        source_language=source_language,
        target_language=target_language,
        format_="text",
    )

    return [r.get("translatedText", "") for r in results]


def process_streaming_transcript_for_translation(
    transcript: str,
    is_final: bool,
    source_language: str = "en",
    target_language: str = "es",
) -> Optional[str]:
    """Process a streaming transcript event and return translated caption if appropriate.

    Only returns a translation for final results to avoid redundant API calls
    on interim partial transcripts.

    Args:
        transcript: The transcript text from speech recognition.
        is_final: Whether this is a final recognition result.
        source_language: Source language code.
        target_language: Target language code.

    Returns:
        Translated text or None if this is an interim result.
    """
    if not is_final:
        return None

    cleaned = clean_transcript_text(transcript)
    if not cleaned:
        return None

    return translate_caption(
        cleaned,
        source_language=source_language,
        target_language=target_language,
    )


def stream_translated_captions(
    transcript_events,
    source_language: str = "en",
    target_language: str = "es",
):
    """Process a stream of recognition events and yield translated captions.

    Args:
        transcript_events: Iterator of (transcript, is_final, confidence) tuples
            from Google Cloud Speech-to-Text.
        source_language: Source language code.
        target_language: Target language code.

    Yields:
        Tuples of (original_transcript, translated_text, is_final, confidence).
    """
    for transcript, is_final, confidence in transcript_events:
        translation = process_streaming_transcript_for_translation(
            transcript,
            is_final,
            source_language,
            target_language,
        )
        yield transcript, translation, is_final, confidence
