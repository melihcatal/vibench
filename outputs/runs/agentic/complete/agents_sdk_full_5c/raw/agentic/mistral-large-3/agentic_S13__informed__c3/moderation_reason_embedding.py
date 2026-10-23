import os
from typing import List
import cohere
from safety_models import SafetyCategory


def embed_moderation_rationales(rationales: List[str]) -> List[List[float]]:
    """
    Embed moderation rationales for case retrieval using Cohere.
    Returns list of embedding vectors.
    """
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(
        texts=rationales,
        model="embed-english-v3.0",
        input_type="search_document"
    )
    return response.embeddings