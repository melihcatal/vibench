import os
import cohere
from typing import List


def embed_transcript_segments(segments: List[str]) -> List[List[float]]:
    """
    Embeds transcript segments for semantic retrieval using Cohere.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=segments, model="embed-english-v3.0", input_type="search_document"
    )

    return response.embeddings
