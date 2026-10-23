import os
from typing import List
import cohere

def log_embedding(messages: List[str]) -> List[List[float]]:
    client = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = client.embed(
        texts=messages,
        model="embed-english-v3.0",
        input_type="search_query"
    )
    return response.embeddings