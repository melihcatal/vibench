import os
from typing import AsyncGenerator, List
from openai import AsyncOpenAI

from speech_models import TranscriptResult


async def get_embedding(text: str) -> List[float]:
    client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    if not client.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    response = await client.embeddings.create(
        model="text-embedding-ada-002", input=[text]
    )
    return response.data[0].embedding


async def caption_embedding(caption_stream: AsyncGenerator[TranscriptResult, None]):
    print("Embedding caption chunks for semantic meeting search...")
    async for caption_result in caption_stream:
        if caption_result.is_final and caption_result.text.strip():
            embedding = await get_embedding(caption_result.text)
            print(
                f"Embedding for '{caption_result.text}' generated (first 5 values): {embedding[:5]}..."
            )
            # In a real application, you would store this embedding with the caption text
            # for semantic search.
        yield caption_result
