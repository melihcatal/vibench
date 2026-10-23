import asyncio
import os
from typing import AsyncGenerator, List
from cohere import AsyncClient
from speech_models import TranscriptChunk


async def caption_embedding(
    caption_stream: AsyncGenerator[TranscriptChunk, None],
) -> AsyncGenerator[List[float], None]:
    client = AsyncClient(api_key=os.getenv("COHERE_API_KEY"))
    async for chunk in caption_stream:
        if chunk.is_final and chunk.text.strip():
            response = await client.embed(
                model="embed-english-v3.0",
                texts=[chunk.text],
                input_type="search_query",
            )
            yield response.embeddings[0]
