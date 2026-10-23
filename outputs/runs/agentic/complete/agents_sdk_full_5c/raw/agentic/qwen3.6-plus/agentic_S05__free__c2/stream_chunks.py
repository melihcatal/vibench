"""
Stream audio chunks from an async source using Google Cloud Speech-to-Text.

This module provides utilities for streaming pre-recorded or dynamically
generated audio chunks from async iterators to the Google Cloud Speech-to-Text
streaming recognition API (speech.googleapis.com). Audio data is wrapped into
StreamingRecognizeRequest messages compatible with the Google Cloud client.
"""

import asyncio
import logging
from typing import AsyncIterator, Callable, Awaitable

from google.cloud.speech_v1 import SpeechClient
from google.cloud.speech_v1.types import (
    RecognitionConfig,
    StreamingRecognitionConfig,
    StreamingRecognizeRequest,
    StreamingRecognizeResponse,
)

logger = logging.getLogger(__name__)

GOOGLE_CLOUD_SPEECH_API_ENDPOINT = "speech.googleapis.com"
GOOGLE_SPEECH_MODEL_ID = "phone_call"


def build_recognition_request(
    audio_bytes: bytes,
    sample_rate_hertz: int = 16000,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = False,
    model: str = GOOGLE_SPEECH_MODEL_ID,
) -> tuple[StreamingRecognizeRequest, StreamingRecognizeRequest]:
    """
    Build a streaming config request and an audio chunk request.

    Returns:
        Tuple of (config_request, audio_request) where the config request
        should be sent first, followed by audio requests for each chunk.
    """
    config = RecognitionConfig(
        model=model,
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
        enable_automatic_punctuation=enable_automatic_punctuation,
        encoding=RecognitionConfig.AudioEncoding.LINEAR16,
    )
    streaming_config = StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    config_request = StreamingRecognizeRequest(streaming_config=streaming_config)
    audio_request = StreamingRecognizeRequest(audio_content=audio_bytes)

    return config_request, audio_request


async def stream_audio_chunks(
    audio_source: AsyncIterator[bytes],
    sample_rate_hertz: int = 16000,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = False,
    on_result: Callable[[dict], Awaitable[None]] | None = None,
) -> AsyncIterator[dict]:
    """
    Stream audio chunks from an async source to Google Cloud Speech-to-Text.

    Args:
        audio_source: Async iterator yielding raw audio bytes (LINEAR16 PCM).
        sample_rate_hertz: Sample rate of the audio stream.
        language_code: BCP-47 language code for recognition.
        enable_automatic_punctuation: Whether to add punctuation automatically.
        on_result: Optional async callback invoked for each recognition result.

    Yields:
        dict: Recognition result data with transcript text and metadata.
    """
    speech_client = SpeechClient()

    config = RecognitionConfig(
        model=GOOGLE_SPEECH_MODEL_ID,
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
        enable_automatic_punctuation=enable_automatic_punctuation,
        encoding=RecognitionConfig.AudioEncoding.LINEAR16,
    )
    streaming_config = StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    async def request_generator():
        yield StreamingRecognizeRequest(streaming_config=streaming_config)

        async for audio_chunk in audio_source:
            logger.debug("Sending audio chunk of %d bytes to %s", len(audio_chunk), GOOGLE_CLOUD_SPEECH_API_ENDPOINT)
            yield StreamingRecognizeRequest(audio_content=audio_chunk)

    responses: AsyncIterator[StreamingRecognizeResponse] = (
        speech_client.streaming_recognize(requests=request_generator())
    )

    async for response in responses:
        for result in response.results:
            if not result.alternatives:
                continue

            best_alt = result.alternatives[0]
            result_data = {
                "text": best_alt.transcript,
                "is_final": result.is_final,
                "confidence": best_alt.confidence,
                "stability": result.stability,
            }

            if on_result is not None:
                await on_result(result_data)

            yield result_data
