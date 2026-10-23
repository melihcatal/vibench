import asyncio
import os
from typing import AsyncGenerator, AsyncIterable, List
from openai import AsyncOpenAI


async def caption_embedding(
    caption_stream: AsyncIterable[str],
) -> AsyncGenerator[List[float], None]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set")
    client = AsyncOpenAI(api_key=api_key)
    async for caption in caption_stream:
        if caption.strip():
            response = await client.embeddings.create(
                model="text-embedding-3-small", input=caption.strip()
            )
            yield response.data[0].embedding
        else:
            yield []
