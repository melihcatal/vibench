import os
import cohere
from typing import List


def embed_caption_chunks(caption_chunks: List[str]):
    """
    Embeds caption chunks for semantic search using Cohere's Embed API.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    try:
        co = cohere.Client(api_key)
        response = co.embed(
            texts=caption_chunks,
            model="embed-english-v3.0",
            input_type="search_document",
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"Cohere API error: {e}")
        return None
