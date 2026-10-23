from typing import AsyncIterable, AsyncIterator

from openai import AsyncOpenAI

from speech_client import load_speech_config


async def stream_chunks(source: AsyncIterable[bytes]) -> AsyncIterator[str]:
    config = load_speech_config("openai", model="gpt-4o-mini-transcribe")
    client = AsyncOpenAI(api_key=config.api_key)
    async for chunk in source:
        if not chunk:
            continue
        result = await client.audio.transcriptions.create(model=config.model, file=chunk, response_format="json")
        text = getattr(result, "text", "")
        if text:
            yield text
