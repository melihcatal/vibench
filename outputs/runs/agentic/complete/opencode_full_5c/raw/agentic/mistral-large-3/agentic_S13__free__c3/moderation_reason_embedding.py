from typing import Dict, List


def embed_moderation_reason(reason: str) -> List[float]:
    """
    Embeds moderation rationales for case retrieval using Cohere Embeddings API.
    Provider: Cohere
    Model: embed-english-v3.0
    """
    import cohere
    import os

    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(
        texts=[reason], model="embed-english-v3.0", input_type="search_document"
    )

    return response.embeddings[0]
