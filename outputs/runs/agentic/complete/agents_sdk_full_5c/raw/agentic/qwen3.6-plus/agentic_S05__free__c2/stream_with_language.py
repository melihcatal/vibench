"""
Start a streaming recognizer with language and punctuation settings using Google Cloud Speech-to-Text.

This module provides a configured streaming speech recognizer that connects to
the Google Cloud Speech API (speech.googleapis.com) with explicit language code,
automatic punctuation, profanity filtering, and model selection.
"""

import asyncio
import logging
from typing import AsyncIterator

from google.cloud.speech_v1 import SpeechClient
from google.cloud.speech_v1.types import (
    RecognitionConfig,
    StreamingRecognitionConfig,
    StreamingRecognizeRequest,
    StreamingRecognizeResponse,
)

logger = logging.getLogger(__name__)

GOOGLE_CLOUD_SPEECH_API_ENDPOINT = "speech.googleapis.com"
GOOGLE_SPEECH_MODEL_DEFAULT = "latest_long"


def create_language_config(
    language_code: str = "en-US",
    alternative_language_codes: list[str] | None = None,
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = True,
    profanity_filter: bool = False,
    model: str = GOOGLE_SPEECH_MODEL_DEFAULT,
    sample_rate_hertz: int = 16000,
    use_enhanced: bool = True,
) -> RecognitionConfig:
    """
    Create a Google Cloud Speech RecognitionConfig with language and punctuation settings.

    Args:
        language_code: Primary BCP-47 language code.
        alternative_language_codes: List of additional language codes to detect.
        enable_automatic_punctuation: Add punctuation to transcribed text.
        enable_word_time_offsets: Include per-word timing information.
        profanity_filter: Filter profane words.
        model: Google Cloud Speech model name (e.g., 'latest_long', 'phone_call').
        sample_rate_hertz: Audio sample rate.
        use_enhanced: Use enhanced models where available.

    Returns:
        Configured RecognitionConfig for Google Cloud Speech-to-Text.
    """
    config_kwargs = {
        "model": model,
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "enable_automatic_punctuation": enable_automatic_punctuation,
        "enable_word_time_offsets": enable_word_time_offsets,
        "profanity_filter": profanity_filter,
        "use_enhanced": use_enhanced,
        "max_alternatives": 3,
    }

    if alternative_language_codes:
        config_kwargs["alternative_language_codes"] = alternative_language_codes

    config = RecognitionConfig(**config_kwargs)
    return config


async def start_streaming_recognizer_with_language(
    audio_request_generator: AsyncIterator[StreamingRecognizeRequest],
    language_code: str = "en-US",
    alternative_language_codes: list[str] | None = None,
    enable_automatic_punctuation: bool = True,
    profanity_filter: bool = False,
    model: str = GOOGLE_SPEECH_MODEL_DEFAULT,
    sample_rate_hertz: int = 16000,
) -> AsyncIterator[dict]:
    """
    Start a streaming recognizer with explicit language and punctuation settings.

    Connects to Google Cloud Speech-to-Text at speech.googleapis.com and yields
    recognition results as they arrive from the streaming API.

    Args:
        audio_request_generator: Async iterator that first yields a config request,
            then yields audio chunk requests.
        language_code: Primary BCP-47 language code.
        alternative_language_codes: Additional languages to detect.
        enable_automatic_punctuation: Enable automatic punctuation insertion.
        profanity_filter: Enable profanity filtering.
        model: Google Cloud Speech model identifier.
        sample_rate_hertz: Audio sample rate in Hz.

    Yields:
        dict: Recognition result with transcript, confidence, and timing data.
    """
    config = create_language_config(
        language_code=language_code,
        alternative_language_codes=alternative_language_codes,
        enable_automatic_punctuation=enable_automatic_punctuation,
        profanity_filter=profanity_filter,
        model=model,
        sample_rate_hertz=sample_rate_hertz,
    )

    streaming_config = StreamingRecognitionConfig(
        config=config,
        interim_results=True,
        single_utterance=False,
    )

    speech_client = SpeechClient()

    logger.info(
        "Starting Google Cloud Speech streaming recognizer (model=%s, language=%s) at %s",
        model,
        language_code,
        GOOGLE_CLOUD_SPEECH_API_ENDPOINT,
    )

    responses: AsyncIterator[StreamingRecognizeResponse] = (
        speech_client.streaming_recognize(requests=audio_request_generator)
    )

    async for response in responses:
        for result in response.results:
            if not result.alternatives:
                continue

            best_alternative = result.alternatives[0]
            word_data = []
            if best_alternative.words:
                for word_info in best_alternative.words:
                    word_data.append({
                        "word": word_info.word,
                        "start_time_ms": int(word_info.start_time.total_seconds() * 1000),
                        "end_time_ms": int(word_info.end_time.total_seconds() * 1000),
                        "confidence": word_info.confidence,
                    })

            yield {
                "text": best_alternative.transcript,
                "is_final": result.is_final,
                "confidence": best_alternative.confidence,
                "stability": result.stability,
                "language_code": language_code,
                "words": word_data,
                "result_index": result.result_index,
            }
