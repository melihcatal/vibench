from typing import AsyncIterator, Iterator

from speech_models import normalize_caption_text


async def stream_chunks(source: AsyncIterator[bytes]) -> Iterator[str]:
    async for chunk in source:
        yield normalize_caption_text(chunk.decode("utf-8", errors="ignore"))
