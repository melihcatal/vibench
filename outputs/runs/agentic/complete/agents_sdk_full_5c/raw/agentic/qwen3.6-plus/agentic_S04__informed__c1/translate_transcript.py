"""Translate completed transcript segments using DeepL API."""

from typing import List, Optional

import deepl

from speech_models import TranscriptionResponse, TranscriptSegment


DEEPL_API_HOST = "api.deepl.com"
DEFAULT_TARGET_LANGUAGE = "en"


def create_deepl_translator(auth_key: Optional[str] = None) -> deepl.Translator:
    """Create a DeepL translator client using the provided auth key."""
    import os
    if auth_key is None:
        auth_key = os.environ.get("DEEPL_AUTH_KEY")
        if not auth_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable must be set")
    return deepl.Translator(auth_key)


def translate_transcript_segments(
    response: TranscriptionResponse,
    target_language: str = "EN",
    auth_key: Optional[str] = None,
) -> TranscriptionResponse:
    """Translate all segments of a transcription response using DeepL.

    Args:
        response: The TranscriptionResponse to translate.
        target_language: Target language code (e.g., 'EN', 'ES', 'FR', 'DE').
        auth_key: Optional DeepL auth key; falls back to environment.

    Returns:
        A new TranscriptionResponse with translated segment text.
    """
    translator = create_deepl_translator(auth_key)
    texts_to_translate = [seg.text for seg in response.segments if seg.text]

    if not texts_to_translate:
        return response

    results = translator.translate_text(
        texts_to_translate,
        target_lang=target_language,
    )

    translated_segments = []
    for i, seg in enumerate(response.segments):
        if i < len(results):
            translated_text = results[i].text
        else:
            translated_text = seg.text
        translated_segments.append(
            TranscriptSegment(
                text=translated_text,
                start_ms=seg.start_ms,
                end_ms=seg.end_ms,
                speaker=seg.speaker,
                confidence=seg.confidence,
            )
        )

    return TranscriptionResponse(
        job_id=response.job_id,
        text=" ".join(s.text for s in translated_segments),
        segments=translated_segments,
        words=response.words,
        language=target_language.lower(),
        audio_duration_ms=response.audio_duration_ms,
        status=response.status,
    )


def translate_full_text(
    text: str,
    target_language: str = "EN",
    auth_key: Optional[str] = None,
) -> str:
    """Translate a full transcript text using DeepL.

    Args:
        text: The source text to translate.
        target_language: Target language code.
        auth_key: Optional DeepL auth key.

    Returns:
        The translated text.
    """
    translator = create_deepl_translator(auth_key)
    result = translator.translate_text(text, target_lang=target_language)
    return result.text


def detect_language_and_translate(
    response: TranscriptionResponse,
    target_language: str = "EN",
    auth_key: Optional[str] = None,
) -> TranscriptionResponse:
    """Detect source language and translate segments, preserving timing data."""
    translator = create_deepl_translator(auth_key)
    texts = [seg.text for seg in response.segments if seg.text]

    if not texts:
        return response

    translated = translator.translate_text(texts, target_lang=target_language)

    translated_segments = []
    for i, seg in enumerate(response.segments):
        if i < len(translated):
            translated_text = translated[i].text
            detected_source = translated[i].detected_source_lang
        else:
            translated_text = seg.text
            detected_source = None
        translated_segments.append(
            TranscriptSegment(
                text=translated_text,
                start_ms=seg.start_ms,
                end_ms=seg.end_ms,
                speaker=seg.speaker,
                confidence=seg.confidence,
            )
        )

    return TranscriptionResponse(
        job_id=response.job_id,
        text=" ".join(s.text for s in translated_segments),
        segments=translated_segments,
        words=[],
        language=target_language.lower(),
        audio_duration_ms=response.audio_duration_ms,
        status=response.status,
    )


if __name__ == "__main__":
    import json
    import sys
    from speech_models import TranscriptionResponse, TranscriptSegment

    demo_response = TranscriptionResponse(
        job_id="demo",
        text="Hello world, this is a test transcript.",
        segments=[
            TranscriptSegment(text="Hello world", start_ms=0, end_ms=1500),
            TranscriptSegment(text="this is a test transcript", start_ms=1500, end_ms=4000),
        ],
    )
    translated = translate_transcript_segments(demo_response, target_language="DE")
    print(json.dumps({
        "original": demo_response.text,
        "translated": translated.text,
        "language": translated.language,
    }, indent=2))
