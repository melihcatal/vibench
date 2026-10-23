from typing import List
from embeddings_client import get_client
from embeddings_models import MODEL_EMBED, normalize_texts

def embed_batch(texts: List[str]) -> List[List[float]]:
    client = get_client()
    normalized = normalize_texts(texts)
    response = client.embeddings.create(
        model=MODEL_EMBED,
        input=normalized
    )
    return [data.embedding for data in response.data]