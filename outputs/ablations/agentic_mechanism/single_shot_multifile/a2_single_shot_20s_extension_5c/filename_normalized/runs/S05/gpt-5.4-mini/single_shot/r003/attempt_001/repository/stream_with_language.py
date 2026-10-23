from typing import AsyncIterable, AsyncIterator

from openai import AsyncOpenAI

from speech_client import build_openai_async_client, load_speech_config
from speech_models import TranscriptEvent, normalize_transcript_event


async def stream_with_language(chunks: AsyncIterable[bytes], language: str, punctuation: bool = True) -> AsyncIterator[TranscriptEvent]:
    config = load_speech_config()
    client = build_openai_async_client()

    async def files():
        idx = 0
        async for chunk in chunks:
            idx += 1
            yield (f"segment-{idx}.wav", chunk)

    response = await client.audio.transcriptions.create(
        model=config.model,
        file=files(),
        language=language,
        temperature=config.temperature,
        response_format="verbose_json",
        prompt="Use punctuation." if punctuation else None,
    )
    yield normalize_transcript_event(response)
