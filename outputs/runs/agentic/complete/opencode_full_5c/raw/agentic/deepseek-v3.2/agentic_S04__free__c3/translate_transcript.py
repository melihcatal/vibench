import os
from typing import List, Optional
from google.cloud import translate_v2 as translate
from speech_models import NormalizedTranscript


def translate_transcript(
    transcript: NormalizedTranscript,
    target_language: str = "es",
    source_language: Optional[str] = None,
) -> List[str]:
    """
    Translate completed transcript segments using Google Cloud Translation API.

    Args:
        transcript: Normalized transcript to translate
        target_language: Target language code (default: "es" for Spanish)
        source_language: Source language code (auto-detected if None)

    Returns:
        List of translated text chunks
    """
    google_credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not google_credentials:
        raise EnvironmentError(
            "Google Cloud credentials not found. Please set GOOGLE_APPLICATION_CREDENTIALS environment variable."
        )

    client = translate.Client()

    chunks = split_into_chunks_for_translation(transcript)
    translations = []

    for chunk in chunks:
        try:
            result = client.translate(
                chunk,
                target_language=target_language,
                source_language=source_language,
                format_="text",
            )
            translations.append(result["translatedText"])
        except Exception as e:
            raise Exception(f"Google Cloud Translation error: {e}")

    return translations


def split_into_chunks_for_translation(
    transcript: NormalizedTranscript, max_chars: int = 5000
) -> List[str]:
    """
    Split transcript into chunks suitable for translation API limits.

    Args:
        transcript: Normalized transcript
        max_chars: Maximum characters per chunk

    Returns:
        List of text chunks
    """
    text = transcript.text
    if len(text) <= max_chars:
        return [text]

    chunks = []
    sentences = text.split(". ")
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        if sentence[-1] != ".":
            sentence += "."

        if len(current_chunk) + len(sentence) + 2 <= max_chars:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def translate_with_preserved_segments(
    transcript: NormalizedTranscript, target_language: str = "es"
) -> List[dict]:
    """
    Translate transcript while preserving segment structure.

    Args:
        transcript: Normalized transcript with segments
        target_language: Target language code

    Returns:
        List of dictionaries with original and translated segments
    """
    google_credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not google_credentials:
        raise EnvironmentError(
            "Google Cloud credentials not found. Please set GOOGLE_APPLICATION_CREDENTIALS environment variable."
        )

    client = translate.Client()

    translated_segments = []

    for segment in transcript.segments:
        try:
            result = client.translate(
                segment.text, target_language=target_language, format_="text"
            )

            translated_segments.append(
                {
                    "original_text": segment.text,
                    "translated_text": result["translatedText"],
                    "start_time": segment.start_time,
                    "end_time": segment.end_time,
                    "confidence": segment.confidence,
                    "detected_source_language": result.get(
                        "detectedSourceLanguage", transcript.language
                    ),
                }
            )
        except Exception as e:
            raise Exception(f"Google Cloud Translation error for segment: {e}")

    return translated_segments
