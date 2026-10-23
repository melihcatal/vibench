import cohere
import os
from typing import List

co = cohere.Client(v1=os.getenv("COHERE_API_KEY"))


def moderation_reason_embedding(reason: str) -> List[float]:
    """
    Embed moderation rationales for case retrieval using Cohere Embed.
    """
    embedding = co.embed(
        texts=[reason], model="embed-english-v3.0", input_type="search_query"
    ).embeddings
    return embedding[0]
