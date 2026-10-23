import os
import cohere
from typing import List

co = cohere.Client(os.getenv("COHERE_API_KEY"))


def moderation_reason_embedding(reason: str) -> List[float]:
    response = co.embed(
        texts=[reason], model="embed-english-v3.0", input_type="search_query"
    )
    return response.embeddings[0]
