import os
import cohere
from typing import List[float]

def moderation_reason_embedding(reason: str) -> List[float]:
    client = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = client.embed(
        texts=[reason],
        model="embed-english-v3.0"
    )
    return response.embeddings[0]