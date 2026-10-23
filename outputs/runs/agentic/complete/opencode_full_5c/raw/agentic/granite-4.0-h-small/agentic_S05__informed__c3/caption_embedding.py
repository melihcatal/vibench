# Embed caption chunks for semantic meeting search
# Service: OpenAI Embeddings API (text embedding)
# SDK: openai
# Authentication: OPENAI_API_KEY

import os
import openai
from typing import AsyncIterable, AsyncIterator

# Configure the OpenAI client once (env var supplied by caller)
openai.api_key = os.getenv("OPENAI_API_KEY")

# OpenAI model identifier (use the desired embedding model)
EMBEDDING_MODEL = "text-embedding-3-large"


async def embed_caption_chunks(source: AsyncIterable[str]) -> AsyncIterable[dict]:
    """Yield embedding dict for each caption chunk.","""
    for chunk in source:
        response = openai.Embedding.create(model=EMBEDDING_MODEL, input=chunk)
        embedding = response["data"][0]["embedding"]
        yield {"chunk": chunk, "embedding": embedding}


# Example placeholder usage (requires full async driver)
# async for emb in embed_caption_chunks(caption_stream()):
#     print("Embedding:", emb['embedding'])
