import asyncio
import os
from openai import AsyncOpenAI
from typing import AsyncGenerator, List[float]

async def embed_caption_chunks(
    caption_gen: AsyncGenerator[str, None]
) -> AsyncGenerator[List[float], None]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    client = AsyncOpenAI(api_key=api_key)

    async for caption in caption_gen:
        if caption.strip():
            response = await client.embeddings.create(
                model="text-embedding-3-small",
                input=caption
            )
            embedding = response.data[0].embedding
            yield embedding
