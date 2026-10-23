import os
import cohere
from typing import List[float]

def embed_moderation_rationale(reason: str) -> List[float]:
    """
    Embeds moderation rationales for case retrieval using Cohere.
    """
    client = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = client.embed(
        texts=[reason],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    return response.embeddings[0]
