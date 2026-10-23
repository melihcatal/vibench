import os
import cohere
from typing import List


def embed_moderation_reasons(reasons: List[str]) -> List[List[float]]:
    """
    Embeds a list of moderation rationales using Cohere's embedding API.
    """
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(cohere_api_key)

    response = co.embed(
        texts=reasons, model="embed-english-v3.0", input_type="search_document"
    )

    return response.embeddings
