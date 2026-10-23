import os
import cohere
from typing import List


def transcript_embedding(transcript_segments: List[str]) -> List[List[float]]:
    co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))
    response = co.embed(
        texts=transcript_segments, model="embed-english-v3.0", input_type="search_query"
    )
    return response.embeddings
