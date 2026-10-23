import os
from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding_response, EmbeddingRequest

MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_text(text: str):
    client = get_embeddings_client()
    req = EmbeddingRequest(input=text, model=MODEL)
    response = client.embeddings.create(model=req.model, input=req.input)
    return normalize_embedding_response(response)
