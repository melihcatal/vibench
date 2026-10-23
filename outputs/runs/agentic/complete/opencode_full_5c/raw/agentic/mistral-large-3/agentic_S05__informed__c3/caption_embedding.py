import os
from openai import OpenAI
from typing import AsyncIterable, List

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def embed_text(text: str) -> List[float]:
    """Embeds text using OpenAI's text-embedding-3-small model."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding


async def caption_embedding(caption_chunks: AsyncIterable[List[str]]):
    """Embeds caption chunks for semantic meeting search."""
    async for chunk in caption_chunks:
        text = " ".join(chunk)
        embedding = await embed_text(text)
        yield {
            "text": text,
            "embedding": embedding,
        }
