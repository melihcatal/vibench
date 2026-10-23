import asyncio
from typing import AsyncIterable, AsyncIterator, Optional

from openai import AsyncOpenAI

from speech_client import build_openai_async_client, load_speech_config
from speech_models import TranscriptEvent, normalize_transcript_event


async def stream_chunks(chunks: AsyncIterable[bytes], language: Optional[str] = None) -> AsyncIterator[TranscriptEvent]:
    config = load_speech_config()
    client = build_openai_async_client()
    model = config.model

    async def files() -> AsyncIterator[tuple[str, bytes]]:
        idx = 0
        async for chunk in chunks:
            idx += 1
            yield (f"chunk-{idx}.wav", chunk)

    response = await client.audio.transcriptions.create(
        model=model,
        file=files(),
        language=language or config.language,
        temperature=config.temperature,
        response_format="verbose_json",
    )
    yield normalize_transcript_event(response)
