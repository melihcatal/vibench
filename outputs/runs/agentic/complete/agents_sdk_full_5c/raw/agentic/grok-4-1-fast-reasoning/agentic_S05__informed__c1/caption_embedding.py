import asyncio
import os
from cohere import Client
from typing import AsyncGenerator

COHERE_API_KEY = os.getenv('COHERE_API_KEY')

async def embed_caption_chunks(
    caption_chunks
) -> AsyncGenerator[list[float], None]:
    if not COHERE_API_KEY:
        raise ValueError('COHERE_API_KEY environment variable is required.')
    client = Client(COHERE_API_KEY)
    async for chunk in caption_chunks:
        if chunk.strip():
            response = await asyncio.to_thread(
                client.embed,
                texts=[chunk],
                model='embed-english-v3.0',
                input_type='search_query'
            )
            yield response.embeddings[0]
