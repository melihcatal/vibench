from typing import List
from safety_client import cohere_client

def moderation_reason_embedding(reason: str) -> List[float]:
    client = cohere_client()
    response = client.embed(
        texts=[reason],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    return response.embeddings[0]