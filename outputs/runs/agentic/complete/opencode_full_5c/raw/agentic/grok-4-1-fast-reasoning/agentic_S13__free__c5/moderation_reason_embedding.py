import os
import cohere
from typing import List


def moderation_reason_embedding(rationale: str) -> List[float]:
    client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))
    response = client.embed(
        model="embed-english-v3.0", texts=[rationale], input_type="search_query"
    )
    return response.embeddings[0]
