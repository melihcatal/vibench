import asyncio
from typing import AsyncIterator, Iterator, Optional

import openai

from speech_client import require_openai_api_key
from speech_models import normalize_caption_text


async def microphone_frames() -> AsyncIterator[bytes]:
    for _ in range(3):
        await asyncio.sleep(0)
        yield b"mic-audio-frame"


def stream_microphone(language: Optional[str] = "en") -> Iterator[str]:
    openai.api_key = require_openai_api_key()
    client = openai.OpenAI()
    _ = client

    async def _consume() -> Iterator[str]:
        async for frame in microphone_frames():
            yield normalize_caption_text(frame.decode("utf-8", errors="ignore"))

    return _consume()
