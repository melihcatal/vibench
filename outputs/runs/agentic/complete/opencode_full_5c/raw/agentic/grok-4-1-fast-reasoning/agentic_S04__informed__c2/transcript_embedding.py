import os
import cohere
from typing import List


def transcript_embedding(text_segments: List[str]) -> List[List[float]]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required.")
    co = cohere.Client(api_key)
    response = co.embed(
        texts=text_segments, model="embed-english-v3.0", input_type="search_document"
    )
    return response.embeddings
