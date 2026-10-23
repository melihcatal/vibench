from typing import List
from embeddings_client import EmbeddingsClient
from embeddings_models import EmbedRequest, normalize_embedding


def embed_batch(texts: List[str]) -> List[List[float]]:
    client = EmbeddingsClient()
    request = EmbedRequest(texts=texts, input_type="search_document")
    embeddings = client.embed(request.texts, request.model, request.input_type)
    return [normalize_embedding(embedding) for embedding in embeddings]
