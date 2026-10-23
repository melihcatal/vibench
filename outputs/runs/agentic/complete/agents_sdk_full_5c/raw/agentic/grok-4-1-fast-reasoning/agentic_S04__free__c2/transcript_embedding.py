import cohere
import os
from typing import List

co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))

def transcript_embedding(segments: List[str]) -> List[List[float]]:
    """
    Embed transcript segments for semantic retrieval using Cohere.
    """
    response = co.embed(
        texts=segments,
        model="embed-english-v3.0"
    )
    return response.embeddings