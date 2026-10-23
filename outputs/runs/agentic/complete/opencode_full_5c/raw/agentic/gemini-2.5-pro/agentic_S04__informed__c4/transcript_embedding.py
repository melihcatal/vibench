import os
from typing import List
import cohere

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY environment variable not set.")

co = cohere.Client(COHERE_API_KEY)


def transcript_embedding(segments: List[str]) -> List[List[float]]:
    """
    Embeds transcript segments for semantic retrieval using Cohere.
    """
    if not segments:
        return []

    response = co.embed(
        texts=segments, model="embed-english-v3.0", input_type="search_document"
    )
    return response.embeddings
