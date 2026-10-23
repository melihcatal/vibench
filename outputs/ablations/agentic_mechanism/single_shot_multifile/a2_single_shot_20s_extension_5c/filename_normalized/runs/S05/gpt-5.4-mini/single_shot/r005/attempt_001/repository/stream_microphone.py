import asyncio
import os
from typing import AsyncIterator, Optional

from speech_client import StreamingSpeechClient, get_speech_client
from speech_models import AudioChunk, TranscriptEvent


async def stream_microphone(sample_rate_hz: int = 16000, language_code: str = "en-US") -> AsyncIterator[TranscriptEvent]:
    client = get_speech_client()
    async for event in client.stream_microphone(sample_rate_hz=sample_rate_hz, language_code=language_code):
        yield event


async def main() -> None:
    async for event in stream_microphone():
        print(event.text)


if __name__ == "__main__":
    asyncio.run(main())
