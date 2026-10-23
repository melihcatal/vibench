import os
import cohere
from typing import List, Any

co = cohere.Client(os.getenv("COHERE_API_KEY"))

def embed_caption_chunks(caption_chunks: List[str]) -> List[List[float]]:
    """
    Embed multiple caption chunks for semantic search.
    """
    if not caption_chunks:
        return []
    response = co.embed(
        texts=caption_chunks,
        model="embed-english-v3.0",
        input_type="search_document",
        embedding_types=["FLOAT"]
    )
    return [emb for emb in response.embeddings["FLOAT"]]
