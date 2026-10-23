from typing import List
from safety_client import get_cohere_client
from safety_models import EmbeddingResponse


def embed_moderation_reasons(reasons: List[str]) -> EmbeddingResponse:
    """
    Embed moderation rationales for case retrieval using Cohere's Embed API.
    """
    client = get_cohere_client()

    response = client.embed(
        texts=reasons, model="embed-english-v3.0", input_type="search_document"
    )

    return EmbeddingResponse(embeddings=response.embeddings)
