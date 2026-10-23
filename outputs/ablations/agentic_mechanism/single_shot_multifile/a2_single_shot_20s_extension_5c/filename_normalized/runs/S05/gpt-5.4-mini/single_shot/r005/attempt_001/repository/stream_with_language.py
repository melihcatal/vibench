import asyncio
from typing import AsyncIterator

from speech_client import get_speech_client
from speech_models import AudioChunk, TranscriptEvent


async def stream_with_language(language_code: str = "en-US", enable_punctuation: bool = True) -> AsyncIterator[TranscriptEvent]:
    client = get_speech_client()
    async for event in client.stream_with_language(language_code=language_code, enable_punctuation=enable_punctuation):
        yield event


async def main() -> None:
    async for event in stream_with_language():
        print(event.text)


if __name__ == "__main__":
    asyncio.run(main())
