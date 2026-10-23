"""
Translate completed transcript segments using DeepL API.

Translates each segment of a transcript into a target language using the
DeepL translation service, preserving speaker labels and structure.
"""

import os
from typing import List, Optional

import requests

from speech_models import TranscriptionSegment, TranscriptionResult


def translate_text(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
) -> str:
    """
    Translate a single text string using the DeepL API.

    Args:
        text: The source text to translate.
        target_lang: Target language code (e.g., 'FR', 'DE', 'ES', 'JA').
        source_lang: Optional source language code (e.g., 'EN'). If None, auto-detect.
        formality: Optional formality level ('more' or 'less') for supported languages.

    Returns:
        Translated text string.

    Raises:
        requests.HTTPError: If the DeepL API returns an error.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY environment variable is required")

    endpoint = "https://api-free.deepl.com/v2/translate"

    payload = {
        "text": text,
        "target_lang": target_lang,
        "auth_key": auth_key,
    }

    if source_lang:
        payload["source_lang"] = source_lang

    if formality:
        payload["formality"] = formality

    response = requests.post(endpoint, data=payload)
    response.raise_for_status()

    result = response.json()
    translations = result.get("translations", [])
    if translations:
        return translations[0].get("text", text)

    return text


def translate_segments(
    segments: List[TranscriptionSegment],
    target_lang: str,
    source_lang: Optional[str] = None,
    preserve_formatting: bool = True,
) -> List[TranscriptionSegment]:
    """
    Translate a list of transcript segments using DeepL API.

    Each segment's text is translated individually while preserving
    speaker labels and timing information.

    Args:
        segments: List of TranscriptionSegment objects.
        target_lang: Target language code for DeepL (e.g., 'FR', 'DE', 'ES').
        source_lang: Optional source language code. Auto-detect if None.
        preserve_formatting: Whether to keep speaker labels intact during translation.

    Returns:
        New list of TranscriptionSegment objects with translated text.
    """
    translated = []

    for segment in segments:
        text_to_translate = segment.text
        translated_text = translate_text(
            text=text_to_translate,
            target_lang=target_lang,
            source_lang=source_lang,
        )

        translated.append(
            TranscriptionSegment(
                text=translated_text,
                speaker_label=segment.speaker_label,
                start_time_ms=segment.start_time_ms,
                end_time_ms=segment.end_time_ms,
                confidence=segment.confidence,
            )
        )

    return translated


def translate_transcript(
    transcript_result: TranscriptionResult,
    target_lang: str,
    source_lang: Optional[str] = None,
) -> TranscriptionResult:
    """
    Full workflow: translate all segments of a TranscriptionResult using DeepL.

    Args:
        transcript_result: The source TranscriptionResult to translate.
        target_lang: Target DeepL language code.
        source_lang: Optional source language code.

    Returns:
        New TranscriptionResult with all segments translated.
    """
    translated_segments = translate_segments(
        segments=transcript_result.segments,
        target_lang=target_lang,
        source_lang=source_lang,
    )

    translated_display = " ".join(s.text for s in translated_segments)

    return TranscriptionResult(
        display_text=translated_display,
        segments=translated_segments,
        locale=target_lang.lower(),
        duration_ms=transcript_result.duration_ms,
    )


def translate_batch(
    texts: List[str],
    target_lang: str,
    source_lang: Optional[str] = None,
) -> List[str]:
    """
    Translate multiple texts in a single DeepL API call for efficiency.

    Args:
        texts: List of text strings to translate.
        target_lang: Target DeepL language code.
        source_lang: Optional source language code.

    Returns:
        List of translated text strings.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY environment variable is required")

    endpoint = "https://api-free.deepl.com/v2/translate"

    payload = {
        "text": texts,
        "target_lang": target_lang,
        "auth_key": auth_key,
    }

    if source_lang:
        payload["source_lang"] = source_lang

    response = requests.post(endpoint, data=payload)
    response.raise_for_status()

    result = response.json()
    translations = result.get("translations", [])

    return [t.get("text", orig) for t, orig in zip(translations, texts)]
