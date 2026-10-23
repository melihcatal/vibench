"""Starts a streaming recognizer with language and punctuation settings using Deepgram Streaming Speech-to-Text."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterable
from typing import Any, AsyncIterator, Callable

from deepgram import DeepgramClient, LiveOptions

from speech_client import create_deepgram_client, build_live_options
from speech_models import (
    PartialTranscript,
    FinalTranscript,
    normalize_deepgram_interim,
    normalize_deepgram_final,
)


SUPPORTED_LANGUAGES = [
    "en", "es", "fr", "de", "it", "pt", "nl", "ja", "ko",
    "zh", "ar", "ru", "hi", "tr", "pl", "sv", "da", "fi",
    "no", "cs", "el", "hu", "ro", "th", "vi", "id", "ms",
]


class LanguageNotSupportedError(ValueError):
    """Raised when a language code is not supported by Deepgram."""
    pass


def validate_language(language: str) -> str:
    """Validate that the language code is supported by Deepgram."""
    normalized = language.strip().lower()
    if normalized not in SUPPORTED_LANGUAGES:
        raise LanguageNotSupportedError(
            f"Language '{language}' is not supported. "
            f"Supported languages: {', '.join(SUPPORTED_LANGUAGES)}"
        )
    return normalized


async def stream_with_language(
    audio_source: AsyncIterable[bytes],
    language: str = "en",
    model: str = "nova-2",
    punctuate: bool = True,
    smart_format: bool = True,
    profanity_filter: bool = False,
    redact: list[str] | None = None,
    interim_results: bool = True,
    channels: int = 1,
    sample_rate: int = 16000,
    on_interim: Callable[[PartialTranscript], None] | None = None,
    on_final: Callable[[FinalTranscript], None] | None = None,
    **extra_kwargs: Any,
) -> AsyncIterator[PartialTranscript | FinalTranscript]:
    """
    Start a Deepgram streaming recognizer with explicit language and punctuation settings.

    Parameters
    ----------
    audio_source : AsyncIterable[bytes]
        Async iterable of raw PCM audio chunks.
    language : str
        ISO 639-1 language code (e.g. "en", "es", "ja").
    model : str
        Deepgram model identifier.
    punctuate : bool
        Enable automatic punctuation.
    smart_format : bool
        Apply smart formatting (numbers, dates, etc.).
    profanity_filter : bool
        Filter profanity from transcripts.
    redact : list[str] | None
        List of PII types to redact (e.g. ["pci", "ssn"]).
    interim_results : bool
        Whether to yield interim results.
    channels : int
        Number of audio channels.
    sample_rate : int
        Audio sample rate in Hz.
    """
    language = validate_language(language)

    options = build_live_options(
        model=model,
        language=language,
        sample_rate=sample_rate,
        channels=channels,
        interim_results=interim_results,
        punctuate=punctuate,
        smart_format=smart_format,
        profanity_filter=profanity_filter,
        redact=redact or [],
        **extra_kwargs,
    )

    client = create_deepgram_client()

    async with client.listen.async_live.v("1").stream(options) as stream:
        async for chunk in audio_source:
            await stream.send(chunk)

        await stream.send({"type": "CloseStream"})

        async for result in stream:
            if result.is_final:
                transcript = normalize_deepgram_final(result)
                if on_final:
                    on_final(transcript)
                yield transcript
            else:
                transcript = normalize_deepgram_interim(result)
                if on_interim:
                    on_interim(transcript)
                yield transcript
