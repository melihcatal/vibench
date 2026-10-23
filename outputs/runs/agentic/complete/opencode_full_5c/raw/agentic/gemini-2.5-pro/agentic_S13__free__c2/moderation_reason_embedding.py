from typing import List
from safety_client import get_cohere_client


def embed_moderation_reasons(reasons: List[str]) -> List[List[float]]:
    """
    Embeds moderation rationales for case retrieval using Cohere's embedding API.
    """
    co = get_cohere_client()

    response = co.embed(
        texts=reasons, model="embed-english-v3.0", input_type="search_document"
    )

    return response.embeddings
