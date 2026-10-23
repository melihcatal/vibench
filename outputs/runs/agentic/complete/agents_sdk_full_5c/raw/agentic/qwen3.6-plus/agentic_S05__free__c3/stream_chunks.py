"""
Stream audio chunks from an async source to Google Cloud Speech-to-Text.

Reads audio data from an async iterable and streams it to the
google.cloud.speech.SpeechClient.streaming_recognize API,
yielding streaming recognition responses as they arrive.
"""

import asyncio
from typing import AsyncGenerator, AsyncIterable

from google.cloud import speech

from speech_client import create_speech_client, get_streaming_config
from speech_models import (
    InterimTranscript,
    FinalTranscript,
    parse_streaming_response,
    build_initial_streaming_request,
    normalize_transcript_text,
)


async def async_audio_chunk_generator(
    audio_source: AsyncIterable[bytes],
) -> AsyncGenerator[bytes, None]:
    """
    Wrap an async audio source and yield raw bytes chunks.

    Designed to work with async audio sources like async file readers,
    network streams, or async microphone interfaces.

    Args:
        audio_source: An async iterable yielding bytes of audio data.

    Yields:
        Raw audio bytes ready for Speech-to-Text streaming.
    """
    async for chunk in audio_source:
        if chunk:
            yield chunk


def _sync_audio_generator(audio_source) -> AsyncGenerator:
    """Convert a synchronous audio source to an async generator."""
    async def _gen():
        for chunk in audio_source:
            if chunk:
                yield chunk
    return _gen()


async def stream_chunks(
    audio_source: AsyncIterable[bytes] | list,
    sample_rate_hertz: int = 16000,
    language_code: str = "en-US",
    enable_punctuation: bool = True,
    model: str = "default",
) -> AsyncGenerator[dict, None]:
    """
    Stream audio chunks from an async source to Google Cloud Speech-to-Text.

    Sends audio chunks from the provided async iterable to
    google.cloud.speech.SpeechClient.streaming_recognize and yields
    normalized transcript results (interim and final) as they arrive.

    Args:
        audio_source: Async iterable or list of bytes chunks.
        sample_rate_hertz: Audio sample rate.
        language_code: BCP-47 language code.
        enable_punctuation: Enable automatic punctuation.
        model: Google recognition model (default, phone_call, video, command_and_search).

    Yields:
        Dict with keys: 'type' ('interim'|'final'), 'text', 'confidence', 'raw'.
    """
    client = create_speech_client()

    streaming_config = get_streaming_config(
        sample_rate_hertz=sample_rate_hertz,
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
        model=model,
    )

    initial_request = build_initial_streaming_request(streaming_config)

    async def request_generator():
        yield initial_request
        if isinstance(audio_source, (list, tuple)):
            for chunk in audio_source:
                yield speech.StreamingRecognizeRequest(audio_content=chunk)
        else:
            async for chunk in audio_source:
                yield speech.StreamingRecognizeRequest(audio_content=chunk)

    loop = asyncio.get_event_loop()

    # Run the blocking streaming_recognize call in a thread pool
    responses = await loop.run_in_executor(
        None,
        lambda: client.streaming_recognize(
            config=streaming_config,
            requests=_sync_request_adapter(request_generator()),
        ),
    )

    for response in responses:
        transcripts = parse_streaming_response(response)
        for t in transcripts:
            result = {
                "raw": t,
                "confidence": t.confidence,
            }
            if isinstance(t, FinalTranscript):
                result["type"] = "final"
                result["text"] = normalize_transcript_text(t.text)
                result["language_code"] = getattr(t, "language_code", language_code)
            else:
                result["type"] = "interim"
                result["text"] = normalize_transcript_text(t.text)
                result["stability"] = getattr(t, "stability", 0.0)
            yield result


def _sync_request_adapter(async_gen):
    """Synchronous wrapper that pulls from an async generator."""
    import asyncio

    loop = asyncio.new_event_loop()

    def _next():
        try:
            return loop.run_until_complete(async_gen.__anext__())
        except StopAsyncIteration:
            raise

    return iter(lambda: _next(), None)
