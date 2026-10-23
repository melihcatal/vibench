import asyncio
from typing import AsyncGenerator, List
from openai import AsyncOpenAI
import os

async def embed_caption_chunks(chunks: AsyncGenerator[str, None]) -> AsyncGenerator[List[float], None]:
    api_key = os.getenv(&quot;OPENAI_API_KEY&quot;)
    if not api_key:
        raise ValueError(&quot;OPENAI_API_KEY environment variable is required&quot;)
    client = AsyncOpenAI(api_key=api_key)
    async for chunk in chunks:
        if chunk.strip():
            response = await client.embeddings.create(
                input=chunk.strip(),
                model=&quot;text-embedding-3-small&quot;
            )
            yield response.data[0].embedding
