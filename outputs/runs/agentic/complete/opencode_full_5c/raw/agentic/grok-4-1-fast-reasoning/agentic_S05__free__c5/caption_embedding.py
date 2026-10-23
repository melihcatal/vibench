import asyncio
import os
from typing import AsyncGenerator, AsyncIterable, List
from openai import AsyncOpenAI


async def embed_caption_chunks(
    caption_iter: AsyncIterable[str],
) -> AsyncGenerator[List[float], None]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    client = AsyncOpenAI(api_key=api_key)
    async for caption in caption_iter:
        if caption.strip():
            response = await client.embeddings.create(
                input=caption, model="text-embedding-3-small"
            )
            yield response.data[0].embedding
