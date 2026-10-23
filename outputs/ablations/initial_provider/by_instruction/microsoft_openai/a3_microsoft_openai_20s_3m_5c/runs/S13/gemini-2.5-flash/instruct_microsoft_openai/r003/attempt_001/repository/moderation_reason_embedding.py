from safety_client import get_cohere_client
from typing import List

def embed_moderation_rationales(rationales: List[str], model: str = "embed-english-v3.0") -> List[List[float]]:
    client = get_cohere_client()
    response = client.embed(
        texts=rationales,
        model=model,
        input_type="classification"
    )
    return response.embeddings
