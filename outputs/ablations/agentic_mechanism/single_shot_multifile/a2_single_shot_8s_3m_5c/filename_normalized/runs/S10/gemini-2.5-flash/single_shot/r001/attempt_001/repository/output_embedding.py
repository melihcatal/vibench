from typing import List
from model_client import get_cohere_client

def embed_text(texts: List[str]) -> List[List[float]]:
    client = get_cohere_client()
    model_id = "embed-english-v3.0"
    response = client.embed(
        texts=texts,
        model=model_id,
        input_type="clustering"
    )
    return response.embeddings