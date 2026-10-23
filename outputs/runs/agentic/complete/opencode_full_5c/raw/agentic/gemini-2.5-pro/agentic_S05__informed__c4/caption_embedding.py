import os
import cohere
from typing import List


async def embed_caption_chunks(caption_chunks: List[str]) -> List[List[float]]:
    """Embeds caption chunks for semantic search using Cohere."""
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.AsyncClient(api_key)

    try:
        response = await co.embed(
            texts=caption_chunks,
            model="embed-english-v3.0",
            input_type="search_document",
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"Error generating embeddings: {e}")
        return []
