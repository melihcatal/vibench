import asyncio
import os
from typing import AsyncGenerator, AsyncIterable, List
from openai import OpenAI
from speech_models import TranscriptChunk

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def embed_caption_chunks(
    transcripts: AsyncIterable[TranscriptChunk],
) -> AsyncGenerator[List[float], None]:
    async for chunk in transcripts:
        if chunk.is_final and chunk.text.strip():
            response = client.embeddings.create(
                input=chunk.text, model="text-embedding-3-small"
            )
            embedding = response.data[0].embedding
            yield embedding
