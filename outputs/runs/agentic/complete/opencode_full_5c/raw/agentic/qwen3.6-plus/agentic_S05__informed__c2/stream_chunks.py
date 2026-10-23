import asyncio
from typing import AsyncGenerator, List, Optional

from speech_models import AudioChunk


async def stream_audio_chunks_from_source(
    source: AsyncGenerator[bytes, None],
    sample_rate: int = 16000,
    channels: int = 1,
) -> AsyncGenerator[AudioChunk, None]:
    async for audio_data in source:
        yield AudioChunk(
            data=audio_data,
            sample_rate=sample_rate,
            channels=channels,
        )


async def stream_audio_chunks_from_list(
    audio_data_list: List[bytes],
    sample_rate: int = 16000,
    channels: int = 1,
    delay_between_chunks: float = 0.0,
) -> AsyncGenerator[AudioChunk, None]:
    for audio_data in audio_data_list:
        yield AudioChunk(
            data=audio_data,
            sample_rate=sample_rate,
            channels=channels,
        )
        if delay_between_chunks > 0:
            await asyncio.sleep(delay_between_chunks)


async def stream_audio_chunks_from_file(
    file_path: str,
    sample_rate: int = 16000,
    channels: int = 1,
    chunk_size: int = 4096,
) -> AsyncGenerator[AudioChunk, None]:
    with open(file_path, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            yield AudioChunk(
                data=data,
                sample_rate=sample_rate,
                channels=channels,
            )


async def stream_audio_chunks_from_queue(
    audio_queue: asyncio.Queue,
    sample_rate: int = 16000,
    channels: int = 1,
    sentinel: Optional[bytes] = None,
) -> AsyncGenerator[AudioChunk, None]:
    while True:
        data = await audio_queue.get()
        if sentinel is not None and data is sentinel:
            break
        if data is None:
            continue
        yield AudioChunk(
            data=data,
            sample_rate=sample_rate,
            channels=channels,
        )


async def stream_audio_chunks_with_backpressure(
    source: AsyncGenerator[bytes, None],
    sample_rate: int = 16000,
    channels: int = 1,
    max_buffer_size: int = 10,
) -> AsyncGenerator[AudioChunk, None]:
    buffer: asyncio.Queue = asyncio.Queue(maxsize=max_buffer_size)
    done_event = asyncio.Event()

    async def producer():
        async for audio_data in source:
            await buffer.put(audio_data)
        done_event.set()

    producer_task = asyncio.create_task(producer())

    try:
        while not done_event.is_set() or not buffer.empty():
            try:
                data = await asyncio.wait_for(buffer.get(), timeout=0.5)
                yield AudioChunk(
                    data=data,
                    sample_rate=sample_rate,
                    channels=channels,
                )
            except asyncio.TimeoutError:
                continue
    finally:
        producer_task.cancel()
