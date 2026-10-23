import os
from typing import List
import cohere


def embed_translated_segments(segments: List[str]) -> List[List[float]]:
    """
    Embeds translated segments for translation-memory search using Cohere Embed API.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")

    co = cohere.Client(api_key)
    response = co.embed(
        texts=segments, model="embed-multilingual-v3.0", input_type="search_document"
    )
    return response.embeddings
