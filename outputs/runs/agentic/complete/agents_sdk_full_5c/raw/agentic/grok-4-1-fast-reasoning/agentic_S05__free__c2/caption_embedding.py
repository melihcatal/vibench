import asyncio
import os
from openai import OpenAI
from typing import AsyncGenerator, List

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def caption_embedding(caption_generator) -> AsyncGenerator[List[float], None]:
    loop = asyncio.get_event_loop()
    async for caption in caption_generator:
        embedding = await loop.run_in_executor(
            None,
            lambda c=caption: client.embeddings.create(
                model="text-embedding-3-small",
                input=c
            ).data[0].embedding
        )
        yield embedding