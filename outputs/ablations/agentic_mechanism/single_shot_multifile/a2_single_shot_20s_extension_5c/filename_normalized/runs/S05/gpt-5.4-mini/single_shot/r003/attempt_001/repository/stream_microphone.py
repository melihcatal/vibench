import asyncio
import os
from typing import AsyncIterator, Iterator, Optional

import sounddevice as sd
from openai import AsyncOpenAI

from speech_client import build_openai_async_client, load_speech_config
from speech_models import TranscriptEvent, normalize_transcript_event


async def stream_microphone(sample_rate: int = 16000, channels: int = 1, blocksize: int = 3200) -> AsyncIterator[TranscriptEvent]:
    config = load_speech_config()
    client = build_openai_async_client()
    model = config.model or os.getenv("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe")

    queue: asyncio.Queue[Optional[bytes]] = asyncio.Queue()

    def callback(indata, frames, time, status):
        if status:
            pass
        queue.put_nowait(bytes(indata))

    stream = sd.RawInputStream(samplerate=sample_rate, channels=channels, dtype="int16", blocksize=blocksize, callback=callback)
    await stream.__aenter__()
    try:
        async def audio_iter() -> AsyncIterator[tuple[str, bytes]]:
            idx = 0
            while True:
                chunk = await queue.get()
                if chunk is None:
                    break
                idx += 1
                yield (f"chunk-{idx}.wav", chunk)

        response = await client.audio.transcriptions.create(
            model=model,
            file=audio_iter(),
            language=config.language,
            temperature=config.temperature,
            response_format="verbose_json",
        )
        yield normalize_transcript_event(response)
    finally:
        await stream.__aexit__(None, None, None)


async def stream_interim_transcripts() -> AsyncIterator[str]:
    async for event in stream_microphone():
        if event.text:
            yield event.text
