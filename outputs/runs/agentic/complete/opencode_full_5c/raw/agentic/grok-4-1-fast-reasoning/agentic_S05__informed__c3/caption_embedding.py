import asyncio
import os
from typing import AsyncGenerator, AsyncIterator, List
from openai import OpenAI


async def embed_caption_chunks(
    caption_chunks: AsyncIterator[str],
) -> AsyncGenerator[List[float], None]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY required")
    client = OpenAI(api_key=api_key)
    loop = asyncio.get_event_loop()
    async for caption in caption_chunks:
        if caption.strip():
            response = await loop.run_in_executor(
                None,
                client.embeddings.create,
                model="text-embedding-3-small",
                input=caption,
            )
            embedding = response.data[0].embedding
            yield embedding
