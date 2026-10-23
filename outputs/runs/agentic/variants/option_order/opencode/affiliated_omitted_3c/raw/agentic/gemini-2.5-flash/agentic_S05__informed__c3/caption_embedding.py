import os
from typing import List
from openai import OpenAI


async def embed_caption_chunks(caption_chunks: List[str]) -> List[List[float]]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    # Provider-specific: OpenAI Embeddings API
    client = OpenAI(api_key=api_key)

    embeddings_list = []
    for chunk in caption_chunks:
        response = client.embeddings.create(
            model="text-embedding-ada-002",  # Provider-specific model identifier
            input=chunk,
        )
        embeddings_list.append(response.data[0].embedding)
    return embeddings_list
