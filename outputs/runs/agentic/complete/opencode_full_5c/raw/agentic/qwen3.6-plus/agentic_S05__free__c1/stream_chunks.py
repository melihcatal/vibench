import asyncio
from typing import AsyncIterator, AsyncIterable

from google.cloud import speech_v2
from google.cloud.speech_v2.types import cloud_speech

from speech_client import SpeechConfig, build_speech_client, build_recognition_config
from speech_models import (
    StreamingResult,
    normalize_streaming_result,
    build_streaming_event,
    StreamingEvent,
)


async def stream_chunks(
    audio_source: AsyncIterable[bytes],
    config: SpeechConfig | None = None,
) -> AsyncIterator[StreamingEvent]:
    cfg = config or SpeechConfig()
    client = build_speech_client(cfg)
    recognition_config = build_recognition_config(cfg)

    streaming_config = cloud_speech.StreamingRecognitionConfig(
        config=recognition_config
    )

    async def request_generator():
        yield cloud_speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        chunk_index = 0
        async for chunk in audio_source:
            chunk_index += 1
            yield cloud_speech.StreamingRecognizeRequest(audio=chunk)

    responses = client.streaming_recognize(requests=request_generator())

    for response in responses:
        for result in response.results:
            normalized = normalize_streaming_result(result)
            event_type = "final" if normalized.is_final else "interim"
            yield build_streaming_event(event_type=event_type, result=normalized)


async def chunked_file_stream(
    filepath: str, chunk_size: int = 3200
) -> AsyncIterable[bytes]:
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk
            await asyncio.sleep(0)


async def chunked_bytes_stream(
    data: bytes, chunk_size: int = 3200
) -> AsyncIterable[bytes]:
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]
        await asyncio.sleep(0)
