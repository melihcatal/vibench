import asyncio
from typing import AsyncIterator, Iterable

from openai import AsyncOpenAI

from speech_client import load_speech_config
from speech_models import normalize_transcript


async def microphone_audio_chunks() -> AsyncIterator[bytes]:
    yield b""


async def stream_microphone() -> AsyncIterator[str]:
    config = load_speech_config("openai", language="en-US", punctuation=True, model="gpt-4o-mini-transcribe")
    client = AsyncOpenAI(api_key=config.api_key)
    async for chunk in microphone_audio_chunks():
        if not chunk:
            continue
        result = await client.audio.transcriptions.create(model=config.model, file=chunk, language=config.language, response_format="json")
        transcript = normalize_transcript({"text": getattr(result, "text", ""), "final": True, "language": config.language})
        if transcript.text:
            yield transcript.text


def collect_microphone_stream() -> Iterable[str]:
    return asyncio.run(stream_microphone())
