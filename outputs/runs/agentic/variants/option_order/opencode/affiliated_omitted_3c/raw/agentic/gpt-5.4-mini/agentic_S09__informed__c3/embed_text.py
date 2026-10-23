import os
import cohere

from embeddings_client import get_embedding_client, DEFAULT_MODEL
from embeddings_models import SingleEmbeddingRequest, normalize_embedding_result


def embed_text(text: str):
    client = get_embedding_client()
    request = SingleEmbeddingRequest(text=text, model=os.getenv("COHERE_EMBED_MODEL", DEFAULT_MODEL))
    response = client.embed(texts=[request.text], model=request.model, input_type="search_document")
    return normalize_embedding_result(response, single_text=request.text)

