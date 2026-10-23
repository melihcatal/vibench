from __future__ import annotations

import asyncio
from typing import AsyncIterator

import sounddevice as sd

from partial_results import PartialTranscriptHandler
from stream_with_language import start_streaming_recognizer


async def stream_microphone_transcripts(
    sample_rate: int = 16000,
    blocksize: int = 1600,
    language_code: str = "en-US",
) -> AsyncIterator[str]:
    queue: asyncio.Queue[bytes] = asyncio.Queue()
    handler = PartialTranscriptHandler()
    emitted = 0

    def _audio_callback(indata, frames, time, status) -> None:
        if status:
            return
        queue.put_nowait(bytes(indata))

    connection = await start_streaming_recognizer(
        language_code=language_code, punctuate=True
    )
    handler.attach(connection)

    with sd.RawInputStream(
        samplerate=sample_rate,
        channels=1,
        dtype="int16",
        blocksize=blocksize,
        callback=_audio_callback,
    ):
        while True:
            chunk = await queue.get()
            await connection.send(chunk)
            if handler.partial_text:
                yield handler.partial_text
            while emitted < len(handler.final_events):
                yield handler.final_events[emitted].text
                emitted += 1
