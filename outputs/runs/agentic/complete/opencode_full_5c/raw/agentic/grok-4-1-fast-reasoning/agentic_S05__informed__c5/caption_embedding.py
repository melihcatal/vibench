import os
import cohere
from typing import AsyncIterator
from speech_models import TranscriptChunk, TranscriptStream

co = cohere.Client(os.getenv("COHERE_API_KEY"))


async def caption_embedding(stream: TranscriptStream) -> AsyncIterator[list[float]]:
    async for chunk in stream:
        text = chunk["transcript"]
        if text.strip():
            response = co.embed(texts=[text], model="embed-english-v3.0")
            yield response.embeddings[0]
