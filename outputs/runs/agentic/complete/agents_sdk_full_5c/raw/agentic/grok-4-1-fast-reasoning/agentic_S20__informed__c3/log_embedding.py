import cohere
import os
from typing import List, Any

def log_embedding(texts: List[str]) -> List[List[float]]:
    client = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = client.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_query"
    )
    return response.embeddings