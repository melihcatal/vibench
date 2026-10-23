import asyncio
import os
from typing import AsyncGenerator, AsyncIterable, List, Any
import openai
from speech_models import Transcript


async def caption_embedding(
    caption_stream: AsyncIterable[Transcript],
    model: str = "text-embedding-3-small",
    api_key: str | None = None,
) -> AsyncGenerator[List[float], None]:
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    client = openai.AsyncOpenAI(api_key=api_key)
    async for transcript in caption_stream:
        if transcript["is_final"]:
            text = transcript["text"].strip()
            if text:
                response = await client.embeddings.create(
                    model=model,
                    input=text,
                )
                embedding = response.data[0].embedding
                yield embedding
