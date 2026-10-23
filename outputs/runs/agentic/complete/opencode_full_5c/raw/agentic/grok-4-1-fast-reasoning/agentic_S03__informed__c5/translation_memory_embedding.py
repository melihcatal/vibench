import cohere
import os
from typing import List


def embed_translation_segments(
    segments: List[str], model: str = "embed-english-v3.0"
) -> List[List[float]]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    co = cohere.Client(api_key)
    response = co.embed(texts=segments, model=model, input_type="search_document")
    return response.embeddings
