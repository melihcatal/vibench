import os
from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding_response, EmbeddingRequest

MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_for_search(query: str, documents):
    client = get_embeddings_client()
    payload = [query] + list(documents)
    req = EmbeddingRequest(input=payload, model=MODEL)
    response = client.embeddings.create(model=req.model, input=req.input)
    vectors = normalize_embedding_response(response)
    return {"query_embedding": vectors[0], "document_embeddings": vectors[1:]}
