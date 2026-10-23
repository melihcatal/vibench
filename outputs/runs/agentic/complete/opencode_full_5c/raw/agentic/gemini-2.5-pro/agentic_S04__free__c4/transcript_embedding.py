import os
import cohere
from typing import List


def embed_transcript_segments(segments: List[str]) -> List[List[float]]:
    """
    Embeds transcript segments for semantic retrieval using Cohere.
    """
    co = cohere.Client(os.environ.get("COHERE_API_KEY"))
    response = co.embed(
        texts=segments,
        model="embed-english-v3.0",
        input_type="search_document",
    )
    return response.embeddings
