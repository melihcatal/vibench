from __future__ import annotations

import asyncio
from typing import AsyncIterator, Iterable

import sounddevice as sd

from speech_client import load_streaming_config, open_stream, stream_audio_chunks
from speech_models import TranscriptEvent, normalize_deepgram_result


async def microphone_audio_source(
    samplerate: int = 16000,
    blocksize: int = 1600,
    channels: int = 1,
    dtype: str = "int16",
) -> AsyncIterator[bytes]:
    queue: asyncio.Queue[bytes] = asyncio.Queue()
    loop = asyncio.get_running_loop()

    def callback(indata, frames, time, status) -> None:
        if status:
            return
        loop.call_soon_threadsafe(queue.put_nowait, bytes(indata))

    stream = sd.RawInputStream(
        samplerate=samplerate,
        blocksize=blocksize,
        channels=channels,
        dtype=dtype,
        callback=callback,
    )
    with stream:
        while True:
            yield await queue.get()


async def stream_microphone_transcripts() -> AsyncIterator[TranscriptEvent]:
    config = load_streaming_config()
    queue: asyncio.Queue[TranscriptEvent] = asyncio.Queue()

    async def on_transcript(result) -> None:
        event = normalize_deepgram_result(result)
        if event.transcript:
            await queue.put(event)

    connection = await open_stream(config, on_transcript)
    sender = asyncio.create_task(
        stream_audio_chunks(connection, microphone_audio_source(config.sample_rate_hz))
    )
    try:
        while True:
            yield await queue.get()
    finally:
        sender.cancel()


async def collect_interim_transcripts(limit: int) -> Iterable[str]:
    transcripts = []
    async for event in stream_microphone_transcripts():
        transcripts.append(event.transcript)
        if len(transcripts) >= limit:
            break
    return transcripts
