import os
import cohere
from typing import List

def translation_memory_embedding(segments: List[str]) -> List[List[float]]:
    """
    Embed translated segments for translation-memory search using Cohere.
    """
    client = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = client.embed(
        texts=segments,
        model="embed-english-v3.0",
        input_type="search_query",
    )
    return response.embeddings
