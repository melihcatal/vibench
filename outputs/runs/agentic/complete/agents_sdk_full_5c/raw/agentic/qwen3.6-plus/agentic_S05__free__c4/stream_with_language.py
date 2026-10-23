"""Starts a streaming recognizer with language and punctuation settings using Google Cloud Speech-to-Text."""

import sys
from typing import Generator, List, Optional

from google.cloud import speech_v1p1beta1 as speech

from speech_client import (
    build_streaming_request_generator,
    create_streaming_recognition_config,
    get_speech_client,
)
from speech_models import StreamingSpeechEvent, normalize_streaming_result, TranscriptSegment


def start_stream_with_language(
    audio_generator,
    language_code: str = "en-US",
    alternative_language_codes: Optional[List[str]] = None,
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = True,
    sample_rate_hertz: int = 16000,
    model: str = "latest_long",
    profanity_filter: bool = False,
    max_alternatives: int = 1,
) -> Generator[StreamingSpeechEvent, None, None]:
    """Start a Google Cloud Speech-to-Text streaming recognizer with specified language and punctuation options.

    Configures the google.cloud.speech_v1p1beta1 client with the given language code,
    optional alternative languages, automatic punctuation, and the 'latest_long' model.

    Args:
        audio_generator: Iterator yielding raw PCM audio bytes (LINEAR16).
        language_code: Primary language code (e.g., "en-US", "es-ES", "fr-FR").
        alternative_language_codes: Secondary language hints for Google Cloud Speech.
        enable_automatic_punctuation: Whether Google Cloud should add punctuation.
        enable_word_time_offsets: Whether to return per-word timing information.
        sample_rate_hertz: Audio sample rate in Hz.
        model: Google Cloud model name (default "latest_long" for long-form audio).
        profanity_filter: Whether to enable Google Cloud profanity masking.
        max_alternatives: Maximum number of alternative hypotheses from Google Cloud.

    Yields:
        StreamingSpeechEvent objects containing transcript segments.
    """
    client = get_speech_client()

    streaming_config = create_streaming_recognition_config(
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
        enable_automatic_punctuation=enable_automatic_punctuation,
        enable_word_time_offsets=enable_word_time_offsets,
        model=model,
        alternative_language_codes=alternative_language_codes,
        max_alternatives=max_alternatives,
        profanity_filter=profanity_filter,
    )

    try:
        requests = build_streaming_request_generator(audio_generator, streaming_config)

        responses = client.streaming_recognize(requests=requests)

        for response in responses:
            event = StreamingSpeechEvent()

            if response.error:
                event.error = f"Google Cloud Speech API error: {response.error.message}"
                yield event
                continue

            if response.results:
                for result in response.results:
                    segment = normalize_streaming_result(result)
                    event.segments.append(segment)

            yield event

    except Exception as exc:
        yield StreamingSpeechEvent(
            error=f"Google Cloud Speech streaming_recognize error: {exc}"
        )


def start_multilingual_stream(
    audio_generator,
    primary_language: str = "en-US",
    secondary_languages: Optional[List[str]] = None,
    enable_automatic_punctuation: bool = True,
    sample_rate_hertz: int = 16000,
) -> Generator[StreamingSpeechEvent, None, None]:
    """Start a multilingual Google Cloud Speech-to-Text stream with primary and secondary languages.

    Uses google.cloud.speech_v1p1beta1 with 'latest_long' model and configures
    alternative_language_codes for code-switching support.
    """
    if secondary_languages is None:
        secondary_languages = ["es-ES", "fr-FR"]

    yield from start_stream_with_language(
        audio_generator=audio_generator,
        language_code=primary_language,
        alternative_language_codes=secondary_languages,
        enable_automatic_punctuation=enable_automatic_punctuation,
        sample_rate_hertz=sample_rate_hertz,
        model="latest_long",
    )


def start_punctuated_stream(
    audio_generator,
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    enable_automatic_punctuation: bool = True,
) -> Generator[TranscriptSegment, None, None]:
    """Start a Google Cloud Speech stream focused on punctuated output.

    Uses google.cloud.speech_v1p1beta1 StreamingRecognize with automatic punctuation
    and the 'latest_long' model, yielding only TranscriptSegment objects.
    """
    for event in start_stream_with_language(
        audio_generator=audio_generator,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        sample_rate_hertz=sample_rate_hertz,
        model="latest_long",
    ):
        if event.error:
            print(f"Error: {event.error}", file=sys.stderr)
            continue
        for segment in event.segments:
            yield segment
