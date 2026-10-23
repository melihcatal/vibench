import asyncio
import os
from typing import AsyncIterator, Optional

import openai


class MicrophoneStreamError(RuntimeError):
    pass


async def stream_microphone(api_key: Optional[str] = None, language: str = "en", model: str = "gpt-4o-mini-transcribe") -> AsyncIterator[str]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise MicrophoneStreamError("OPENAI_API_KEY is required")
    client = openai.AsyncOpenAI(api_key=key)
    stream = await client.audio.transcriptions.create(
        model=model,
        file=None,
        response_format="text",
        language=language,
        stream=True,
    )
    async for event in stream:
        text = getattr(event, "text", None)
        if text:
            yield text


async def iter_microphone_transcripts(api_key: Optional[str] = None, language: str = "en", model: str = "gpt-4o-mini-transcribe") -> AsyncIterator[str]:
    async for transcript in stream_microphone(api_key=api_key, language=language, model=model):
        yield transcript


def run_microphone_stream(api_key: Optional[str] = None, language: str = "en", model: str = "gpt-4o-mini-transcribe") -> None:
    async def _runner() -> None:
        async for _ in stream_microphone(api_key=api_key, language=language, model=model):
            pass

    asyncio.run(_runner())
