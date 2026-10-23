from typing import List
from embeddings_client import EmbeddingsClient
from embeddings_models import EmbedRequest, normalize_embedding


def embed_text(text: str) -> List[float]:
    client = EmbeddingsClient()
    request = EmbedRequest(texts=[text], input_type="search_document")
    embeddings = client.embed(request.texts, request.model, request.input_type)
    return normalize_embedding(embeddings[0])
