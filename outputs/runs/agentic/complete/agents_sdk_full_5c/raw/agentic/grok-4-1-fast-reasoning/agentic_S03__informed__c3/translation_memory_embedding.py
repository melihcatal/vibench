import os
from typing import List
import cohere

co = cohere.Client(os.getenv("COHERE_API_KEY"))

def translation_memory_embedding(segments: List[str]) -> List[list[float]]:
    response = co.embed(
        texts=segments,
        model="embed-english-v3.0",
        input_type="search_document"
    )
    return response.embeddings