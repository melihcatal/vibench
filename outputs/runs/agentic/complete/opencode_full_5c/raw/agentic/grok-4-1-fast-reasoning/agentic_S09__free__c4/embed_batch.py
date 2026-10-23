from typing import List
from embeddings_client import get_cohere_client
from embeddings_models import BatchEmbeddings, normalize_embedding


def embed_batch(texts: List[str], model: str = "embed-english-v3.0") -> BatchEmbeddings:
    client = get_cohere_client()
    response = client.embed(
        model=model, texts=[t.strip() for t in texts], input_type="search_document"
    )
    return [normalize_embedding(emb) for emb in response.embeddings]
