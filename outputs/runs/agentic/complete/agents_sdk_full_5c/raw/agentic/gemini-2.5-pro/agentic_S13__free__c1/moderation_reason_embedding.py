import cohere
from typing import List
from safety_client import safety_clients_config

def embed_moderation_reasons(reasons: List[str]) -> List[List[float]]:
    """
    Embeds moderation rationales for case retrieval using Cohere.
    """
    api_key = safety_clients_config.COHERE_API_KEY
    if not api_key:
        raise ValueError("COHERE_API_KEY is not set.")
    
    co = cohere.Client(api_key)

    response = co.embed(
        texts=reasons,
        model="embed-english-light-v3.0",
        input_type="search_document"
    )

    return response.embeddings
