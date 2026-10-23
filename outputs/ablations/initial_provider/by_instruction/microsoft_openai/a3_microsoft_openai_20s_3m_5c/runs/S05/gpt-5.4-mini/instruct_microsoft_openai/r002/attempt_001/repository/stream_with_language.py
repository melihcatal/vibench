from typing import AsyncIterable, AsyncIterator

from openai import AsyncOpenAI

from speech_client import load_speech_config


async def stream_with_language(source: AsyncIterable[bytes], language: str, punctuation: bool = True) -> AsyncIterator[str]:
    config = load_speech_config("openai", language=language, punctuation=punctuation, model="gpt-4o-mini-transcribe")
    client = AsyncOpenAI(api_key=config.api_key)
    async for chunk in source:
        if not chunk:
            continue
        result = await client.audio.transcriptions.create(model=config.model, file=chunk, language=config.language, response_format="json")
        text = getattr(result, "text", "")
        if punctuation and text and not text.endswith((".", "!", "?")):
            text = f"{text}."
        if text:
            yield text
