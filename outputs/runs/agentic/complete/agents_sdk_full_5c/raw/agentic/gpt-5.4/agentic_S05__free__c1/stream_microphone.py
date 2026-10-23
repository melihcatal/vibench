from __future__ import annotations

import asyncio
from typing import AsyncIterator, Optional

import sounddevice as sd
from google.cloud.speech_v2.types import cloud_speech

from partial_results import extract_transcript_segments
from speech_client import build_streaming_config, create_speech_client, recognizer_name


async def microphone_audio_source(
    *,
    sample_rate_hz: int = 16000,
    blocksize: int = 1600,
    device: Optional[int] = None,
) -> AsyncIterator[bytes]:
    queue: asyncio.Queue[bytes] = asyncio.Queue()
    loop = asyncio.get_running_loop()

    def callback(indata, frames, time, status):
        if status:
            return
        loop.call_soon_threadsafe(queue.put_nowait, bytes(indata))

    stream = sd.RawInputStream(
        samplerate=sample_rate_hz,
        channels=1,
        dtype="int16",
        blocksize=blocksize,
        device=device,
        callback=callback,
    )
    with stream:
        while True:
            yield await queue.get()


async def stream_microphone_transcripts(
    *,
    language_code: str = "en-US",
    model: str = "latest_short",
) -> AsyncIterator[str]:
    client = create_speech_client()
    config = build_streaming_config(
        language_code=language_code,
        model=model,
        interim_results=True,
    )

    async def requests() -> AsyncIterator[cloud_speech.StreamingRecognizeRequest]:
        yield cloud_speech.StreamingRecognizeRequest(
            recognizer=recognizer_name(),
            streaming_config=config,
        )
        async for chunk in microphone_audio_source():
            yield cloud_speech.StreamingRecognizeRequest(audio=chunk)

    responses = await client.streaming_recognize(requests=requests())
    async for response in responses:
        for segment in extract_transcript_segments(response):
            if segment.text:
                yield segment.text
