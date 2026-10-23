import os
import cohere

from embeddings_client import get_embedding_client, DEFAULT_MODEL
from embeddings_models import BatchEmbeddingRequest, normalize_embedding_result


def embed_batch(texts):
    client = get_embedding_client()
    request = BatchEmbeddingRequest(texts=texts, model=os.getenv("COHERE_EMBED_MODEL", DEFAULT_MODEL))
    response = client.embed(texts=request.texts, model=request.model, input_type="search_document")
    return normalize_embedding_result(response)

