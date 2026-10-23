import asyncio
from typing import AsyncIterable, AsyncIterator

import openai


async def stream_chunks(source: AsyncIterable[bytes], model: str = "gpt-5.4-mini") -> AsyncIterator[bytes]:
    client = openai.AsyncOpenAI()
    async for chunk in source:
        if chunk:
            await asyncio.sleep(0)
            yield chunk
