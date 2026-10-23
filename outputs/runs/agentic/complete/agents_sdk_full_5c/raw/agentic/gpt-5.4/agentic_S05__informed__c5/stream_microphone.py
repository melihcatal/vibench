from __future__ import annotations

import asyncio
from typing import AsyncIterator

import sounddevice as sd
from deepgram import LiveTranscriptionEvents

from partial_results import DeepgramPartialResultsHandler
from speech_client import DeepgramStreamingHelper
from speech_models import TranscriptChunk


async def stream_microphone_transcripts(
    *,
    sample_rate_hz: int = 16000,
    blocksize: int = 1600,
    channels: int = 1,
) -> AsyncIterator[TranscriptChunk]:
    helper = DeepgramStreamingHelper()
    connection = await helper.open_connection(sample_rate=sample_rate_hz, channels=channels)
    queue: asyncio.Queue[TranscriptChunk | None] = asyncio.Queue()
    audio_queue: asyncio.Queue[bytes | None] = asyncio.Queue()
    handler = DeepgramPartialResultsHandler()

    async def on_message(_: object, result: object, **__: object) -> None:
        chunk = handler.handle_result(result)
        if chunk is not None:
            await queue.put(chunk)

    async def on_close(_: object, **__: object) -> None:
        await queue.put(None)

    connection.on(LiveTranscriptionEvents.Transcript, on_message)
    connection.on(LiveTranscriptionEvents.Close, on_close)

    loop = asyncio.get_running_loop()

    def audio_callback(indata, frames, time, status) -> None:
        del frames, time, status
        loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))

    stream = sd.RawInputStream(
        samplerate=sample_rate_hz,
        blocksize=blocksize,
        channels=channels,
        dtype="int16",
        callback=audio_callback,
    )

    async def send_audio() -> None:
        with stream:
            while True:
                audio = await audio_queue.get()
                if audio is None:
                    break
                await connection.send(audio)
        await connection.finish()

    sender = asyncio.create_task(send_audio())
    try:
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item
    finally:
        await audio_queue.put(None)
        if not sender.done():
            sender.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await sender


import contextlib
