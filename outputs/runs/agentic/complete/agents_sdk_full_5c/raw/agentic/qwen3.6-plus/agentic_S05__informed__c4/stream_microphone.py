"""Streams microphone audio and yields interim transcripts using Deepgram Streaming Speech-to-Text."""

from __future__ import annotations

import asyncio
import queue
import threading
from typing import AsyncIterator, Callable

try:
    import sounddevice as sd
    import numpy as np
except ImportError:
    raise ImportError(
        "Install audio capture dependencies: pip install sounddevice numpy"
    )

from deepgram import DeepgramClient, LiveOptions

from speech_client import create_deepgram_client, build_live_options
from speech_models import (
    PartialTranscript,
    FinalTranscript,
    normalize_deepgram_interim,
    normalize_deepgram_final,
)


SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 8000  # 0.5 seconds of 16-bit PCM at 16kHz


def _mic_capture_thread(
    audio_queue: queue.Queue,
    stop_event: threading.Event,
    sample_rate: int = SAMPLE_RATE,
    channels: int = CHANNELS,
) -> None:
    """Capture audio from the microphone and push into a queue."""
    def callback(indata, frames, time_info, status):
        if status:
            pass
        audio_queue.put(indata.tobytes())

    with sd.InputStream(
        samplerate=sample_rate,
        channels=channels,
        dtype="int16",
        callback=callback,
    ):
        while not stop_event.is_set():
            sd.sleep(100)


async def stream_microphone(
    model: str = "nova-2",
    language: str = "en",
    punctuate: bool = True,
    on_interim: Callable[[PartialTranscript], None] | None = None,
    on_final: Callable[[FinalTranscript], None] | None = None,
) -> AsyncIterator[PartialTranscript | FinalTranscript]:
    """Stream microphone audio to Deepgram and yield interim and final transcripts."""
    client = create_deepgram_client()
    options = build_live_options(
        model=model,
        language=language,
        punctuate=punctuate,
        sample_rate=SAMPLE_RATE,
        channels=CHANNELS,
    )

    audio_queue: queue.Queue = queue.Queue()
    stop_event = threading.Event()

    capture_thread = threading.Thread(
        target=_mic_capture_thread,
        args=(audio_queue, stop_event),
        daemon=True,
    )
    capture_thread.start()

    try:
        async def audio_generator():
            loop = asyncio.get_event_loop()
            while not stop_event.is_set():
                try:
                    chunk = await loop.run_in_executor(None, audio_queue.get, True, 1.0)
                    yield chunk
                except queue.Empty:
                    continue

        async with client.listen.async_live.v("1").stream(options) as stream:
            async for result in stream:
                if result.is_final:
                    transcript = normalize_deepgram_final(result)
                    if on_final:
                        on_final(transcript)
                    yield transcript
                else:
                    transcript = normalize_deepgram_interim(result)
                    if on_interim:
                        on_interim(transcript)
                    yield transcript

            await stream.send({"type": "CloseStream"})

    finally:
        stop_event.set()
        capture_thread.join(timeout=2.0)
