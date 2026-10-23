"""
Starts a streaming recognizer with language and punctuation settings using Google Cloud Speech-to-Text.
Configures the recognition request with specific language codes, alternate languages,
and automatic punctuation options.

Provider: Google Cloud Speech-to-Text Streaming API
SDK: google-cloud-speech
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

import asyncio
import logging
from collections.abc import AsyncGenerator
from typing import Optional

from google.cloud import speech_v1p1beta1 as speech

from partial_results import handle_streaming_response
from speech_client import (
    build_streaming_config,
    build_streaming_config_with_alternate_languages,
    create_speech_client,
)
from speech_models import PartialTranscriptResult

logger = logging.getLogger(__name__)


async def start_streaming_with_language(
    audio_source: AsyncGenerator[bytes, None],
    language_code: str = "en-US",
    alternate_language_codes: Optional[list[str]] = None,
    enable_automatic_punctuation: bool = True,
    sample_rate_hertz: int = 16000,
    stop_event: Optional[asyncio.Event] = None,
) -> AsyncGenerator[PartialTranscriptResult, None]:
    """
    Start a Google Cloud streaming recognizer with language and punctuation settings.

    Uses the Google Cloud Speech-to-Text streaming API via the google-cloud-speech SDK
    with configurable language codes and alternate language detection.

    Args:
        audio_source: Async generator yielding raw audio bytes.
        language_code: Primary BCP-47 language code (e.g., 'en-US').
        alternate_language_codes: Optional list of alternate language codes for detection.
        enable_automatic_punctuation: Whether to enable automatic punctuation.
        sample_rate_hertz: Audio sample rate.
        stop_event: Optional asyncio.Event to signal stop.

    Yields:
        PartialTranscriptResult objects with interim and final transcripts.
    """
    client = create_speech_client()

    if alternate_language_codes:
        streaming_config = build_streaming_config_with_alternate_languages(
            sample_rate_hertz=sample_rate_hertz,
            language_code=language_code,
            alternate_language_codes=alternate_language_codes,
            enable_automatic_punctuation=enable_automatic_punctuation,
        )
    else:
        streaming_config = build_streaming_config(
            sample_rate_hertz=sample_rate_hertz,
            language_code=language_code,
            enable_automatic_punctuation=enable_automatic_punctuation,
        )

    logger.info(
        f"Starting Google Cloud Speech streaming with language={language_code}, "
        f"alternate_languages={alternate_language_codes}, "
        f"auto_punctuation={enable_automatic_punctuation}"
    )

    async def request_generator():
        config_request = speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        yield config_request

        async for audio_bytes in audio_source:
            audio_request = speech.StreamingRecognizeRequest(audio_content=audio_bytes)
            yield audio_request
            if stop_event and stop_event.is_set():
                break

    responses = client.streaming_recognize(requests=request_generator())

    for response in responses:
        if stop_event and stop_event.is_set():
            break
        partial_results = handle_streaming_response(response)
        for partial in partial_results:
            yield partial


async def start_streaming_with_punctuation_disabled(
    audio_source: AsyncGenerator[bytes, None],
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    stop_event: Optional[asyncio.Event] = None,
) -> AsyncGenerator[PartialTranscriptResult, None]:
    """
    Start a Google Cloud streaming recognizer with punctuation disabled.

    Args:
        audio_source: Async generator yielding raw audio bytes.
        language_code: BCP-47 language code.
        sample_rate_hertz: Audio sample rate.
        stop_event: Optional asyncio.Event to signal stop.

    Yields:
        PartialTranscriptResult objects.
    """
    async for result in start_streaming_with_language(
        audio_source=audio_source,
        language_code=language_code,
        enable_automatic_punctuation=False,
        sample_rate_hertz=sample_rate_hertz,
        stop_event=stop_event,
    ):
        yield result


async def start_streaming_multilingual(
    audio_source: AsyncGenerator[bytes, None],
    primary_language: str = "en-US",
    secondary_languages: Optional[list[str]] = None,
    sample_rate_hertz: int = 16000,
    stop_event: Optional[asyncio.Event] = None,
) -> AsyncGenerator[PartialTranscriptResult, None]:
    """
    Start a multilingual Google Cloud streaming recognizer.

    Automatically detects speech in the primary and secondary languages.

    Args:
        audio_source: Async generator yielding raw audio bytes.
        primary_language: Primary BCP-47 language code.
        secondary_languages: List of secondary language codes.
        sample_rate_hertz: Audio sample rate.
        stop_event: Optional asyncio.Event to signal stop.

    Yields:
        PartialTranscriptResult objects with detected language information.
    """
    if secondary_languages is None:
        secondary_languages = ["es-ES", "fr-FR", "de-DE"]

    async for result in start_streaming_with_language(
        audio_source=audio_source,
        language_code=primary_language,
        alternate_language_codes=secondary_languages,
        enable_automatic_punctuation=True,
        sample_rate_hertz=sample_rate_hertz,
        stop_event=stop_event,
    ):
        yield result
