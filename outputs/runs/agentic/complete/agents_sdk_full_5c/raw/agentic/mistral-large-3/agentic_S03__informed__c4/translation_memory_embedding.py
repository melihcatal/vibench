import os
from cohere import Client
from typing import List

cohere_client = Client(api_key=os.getenv("COHERE_API_KEY"))

def embed_translated_segments(segments: List[str]) -> List[List[float]]:
    response = cohere_client.embed(
        texts=segments,
        model="embed-multilingual-v3.0",
        input_type="search_document"
    )
    return response.embeddings