import asyncio
from typing import AsyncGenerator
from openai import AsyncOpenAI
import os

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def embed_caption_chunks(
    caption_stream: AsyncGenerator[str, None],
) -> AsyncGenerator[list[float], None]:
    async for caption in caption_stream:
        if not caption.strip():
            continue
        response = await client.embeddings.create(
            model="text-embedding-3-small",
            input=caption,
        )
        yield response.data[0].embedding
