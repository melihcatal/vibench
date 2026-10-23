import asyncio
import os
from typing import List
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

async def embed_caption_chunks(
    captions: list[str]
) -> List[List[float]]:
    embeddings = []
    for caption in captions:
        response = await asyncio.to_thread(
            client.embeddings.create,
            model='text-embedding-3-small',
            input=caption
        )
        embeddings.append(response.data[0].embedding)
    return embeddings

async def embed_single_caption(caption: str) -> List[float]:
    response = await asyncio.to_thread(
        client.embeddings.create,
        model='text-embedding-3-small',
        input=caption
    )
    return response.data[0].embedding
