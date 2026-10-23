import asyncio
import os
from openai import OpenAI
from typing import AsyncGenerator, AsyncIterable, List, Any

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

async def caption_embedding(captions: AsyncIterable[str]) -> AsyncGenerator[List[float], None]:
    async for caption in captions:
        if caption.strip():
            response = client.embeddings.create(
                input=caption.strip(),
                model="text-embedding-3-small"
            )
            yield response.data[0].embedding