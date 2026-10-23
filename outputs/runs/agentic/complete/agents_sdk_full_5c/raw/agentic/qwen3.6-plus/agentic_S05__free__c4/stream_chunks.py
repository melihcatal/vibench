"""Streams audio chunks from an async source and sends them to Google Cloud Speech-to-Text streaming API."""

import asyncio
from typing import AsyncGenerator, List, Optional

from google.cloud import speech_v1p1beta1 as speech

from speech_client import create_streaming_recognition_config, get_speech_client, normalize_audio_chunk
from speech_models import StreamingSpeechEvent, normalize_streaming_result


async def stream_audio_chunks(
    chunk_source: AsyncGenerator[bytes, None],
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    model: str = "latest_long",
    enable_automatic_punctuation: bool = True,
) -> AsyncGenerator[StreamingSpeechEvent, None]:
    """Consume an async stream of audio bytes and yield Google Cloud Speech-to-Text transcript events.

    Uses google.cloud.speech_v1p1beta1.SpeechClient.streaming_recognize to process
    audio chunks asynchronously with the specified model.
    """
    streaming_config = create_streaming_recognition_config(
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
        model=model,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )

    # Collect audio chunks into a list, then feed via async generator to sync client
    collected_chunks: List[bytes] = []
    async for chunk in chunk_source:
        normalized = normalize_audio_chunk(chunk)
        collected_chunks.append(normalized)

    def sync_request_generator():
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        for chunk in collected_chunks:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    client = get_speech_client()
    loop = asyncio.get_event_loop()

    try:
        responses = await loop.run_in_executor(
            None,
            lambda: list(client.streaming_recognize(requests=sync_request_generator())),
        )
        for response in responses:
            event = StreamingSpeechEvent()
            if response.results:
                for result in response.results:
                    segment = normalize_streaming_result(result)
                    event.segments.append(segment)
            yield event
    except Exception as exc:
        yield StreamingSpeechEvent(error=f"Google Cloud Speech async streaming error: {exc}")


async def stream_audio_chunks_realtime(
    chunk_source: AsyncGenerator[bytes, None],
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    model: str = "latest_long",
    enable_automatic_punctuation: bool = True,
    chunk_send_interval: float = 0.2,
) -> AsyncGenerator[StreamingSpeechEvent, None]:
    """Stream audio chunks in real-time to Google Cloud Speech-to-Text with interleaved responses.

    Sends each chunk with a configurable delay to simulate real-time streaming,
    using the google.cloud.speech_v1p1beta1 SDK for transcription.
    """
    streaming_config = create_streaming_recognition_config(
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
        model=model,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )

    client = get_speech_client()
    request_queue: asyncio.Queue = asyncio.Queue()

    # Signal config first
    config_request = speech.StreamingRecognizeRequest(streaming_config=streaming_config)

    async def enqueue_audio():
        await request_queue.put(config_request)
        async for chunk in chunk_source:
            normalized = normalize_audio_chunk(chunk)
            await request_queue.put(
                speech.StreamingRecognizeRequest(audio_content=normalized)
            )
            await asyncio.sleep(chunk_send_interval)
        await request_queue.put(None)  # sentinel

    async def request_iter():
        while True:
            item = await request_queue.get()
            if item is None:
                break
            yield item

    producer_task = asyncio.create_task(enqueue_audio())

    try:
        loop = asyncio.get_event_loop()
        responses_future = loop.run_in_executor(
            None,
            lambda: list(client.streaming_recognize(requests=request_iter())),
        )
        responses = await responses_future
        for response in responses:
            event = StreamingSpeechEvent()
            if response.results:
                for result in response.results:
                    segment = normalize_streaming_result(result)
                    event.segments.append(segment)
            yield event
    except Exception as exc:
        yield StreamingSpeechEvent(error=f"Google Cloud Speech realtime async error: {exc}")
    finally:
        producer_task.cancel()
