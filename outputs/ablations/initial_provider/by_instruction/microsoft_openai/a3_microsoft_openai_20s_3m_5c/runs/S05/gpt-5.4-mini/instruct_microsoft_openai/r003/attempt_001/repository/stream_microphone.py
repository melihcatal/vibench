import asyncio
from typing import AsyncIterator

from speech_client import load_config, stream_transcript_events
from speech_models import TranscriptChunk


async def microphone_audio_chunks() -> AsyncIterator[bytes]:
    yield b""


async def stream_microphone() -> AsyncIterator[TranscriptChunk]:
    config = load_config()
    async for chunk in stream_transcript_events(microphone_audio_chunks()):
        yield chunk


def run() -> None:
    async def _main() -> None:
        async for item in stream_microphone():
            _ = item

    asyncio.run(_main())


if __name__ == "__main__":
    run()
