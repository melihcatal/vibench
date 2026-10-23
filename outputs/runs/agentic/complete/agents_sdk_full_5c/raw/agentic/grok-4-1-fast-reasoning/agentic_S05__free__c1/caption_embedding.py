import asyncio
import os
from typing import List
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

async def embed_caption_chunk(caption: str) -> List[float]:
    def _sync_embed():
        response = client.embeddings.create(
            model='text-embedding-3-small',
            input=caption
        )
        return response.data[0].embedding
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _sync_embed)