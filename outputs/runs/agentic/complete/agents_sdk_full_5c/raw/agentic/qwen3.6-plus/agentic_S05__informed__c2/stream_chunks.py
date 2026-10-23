"""
Streams audio chunks from an async source and sends them to Google Cloud Speech-to-Text.
Wraps an asynchronous audio byte source into streaming recognition requests.

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
from speech_client import build_streaming_config, create_speech_client
from speech_models import PartialTranscriptResult

logger = logging.getLogger(__name__)


async def chunk_source_to_requests(
    audio_source: AsyncGenerator[bytes, None],
    streaming_config: speech.StreamingRecognitionConfig,
) -> AsyncGenerator[speech.StreamingRecognizeRequest, None]:
    """
    Convert an async audio byte source into Google Cloud streaming requests.

    Args:
        audio_source: Async generator yielding raw audio bytes.
        streaming_config: Pre-built StreamingRecognitionConfig.

    Yields:
        StreamingRecognizeRequest objects for the Google Cloud Speech API.
    """
    config_request = speech.StreamingRecognizeRequest(streaming_config=streaming_config)
    yield config_request

    async for audio_bytes in audio_source:
        audio_request = speech.StreamingRecognizeRequest(audio_content=audio_bytes)
        yield audio_request


async def stream_audio_chunks(
    audio_source: AsyncGenerator[bytes, None],
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    enable_automatic_punctuation: bool = True,
    stop_event: Optional[asyncio.Event] = None,
) -> AsyncGenerator[PartialTranscriptResult, None]:
    """
    Stream audio chunks from an async source through Google Cloud Speech-to-Text.

    Uses the Google Cloud Speech-to-Text streaming API via the google-cloud-speech SDK.

    Args:
        audio_source: Async generator yielding raw audio bytes.
        language_code: BCP-47 language code for recognition.
        sample_rate_hertz: Audio sample rate.
        enable_automatic_punctuation: Whether to enable auto-punctuation.
        stop_event: Optional asyncio.Event to signal stop.

    Yields:
        PartialTranscriptResult objects with interim and final transcripts.
    """
    client = create_speech_client()

    streaming_config = build_streaming_config(
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )

    request_stream = chunk_source_to_requests(audio_source, streaming_config)

    responses = client.streaming_recognize(requests=request_stream)

    for response in responses:
        if stop_event and stop_event.is_set():
            break
        partial_results = handle_streaming_response(response)
        for partial in partial_results:
            yield partial


async def stream_chunks_from_queue(
    audio_queue: asyncio.Queue,
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    enable_automatic_punctuation: bool = True,
) -> AsyncGenerator[PartialTranscriptResult, None]:
    """
    Stream audio chunks from an asyncio.Queue through Google Cloud Speech-to-Text.

    Args:
        audio_queue: Asyncio queue yielding raw audio bytes. Use None sentinel to stop.
        language_code: BCP-47 language code for recognition.
        sample_rate_hertz: Audio sample rate.
        enable_automatic_punctuation: Whether to enable auto-punctuation.

    Yields:
        PartialTranscriptResult objects with interim and final transcripts.
    """
    async def queue_to_stream():
        while True:
            chunk = await audio_queue.get()
            if chunk is None:
                break
            yield chunk

    async for result in stream_audio_chunks(
        audio_source=queue_to_stream(),
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
        enable_automatic_punctuation=enable_automatic_punctuation,
    ):
        yield result
