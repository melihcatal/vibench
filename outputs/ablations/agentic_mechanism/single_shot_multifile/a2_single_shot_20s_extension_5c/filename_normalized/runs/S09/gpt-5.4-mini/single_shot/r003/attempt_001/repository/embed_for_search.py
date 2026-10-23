import os
from typing import Dict, List, Sequence

from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding_response

MODEL_ID = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_for_search(query: str, documents: List[str]) -> Dict[str, Sequence[float]]:
    client = get_embeddings_client()
    response = client.embeddings.create(model=MODEL_ID, input=[query, *documents])
    embeddings = normalize_embedding_response(response)
    return {"query_embedding": embeddings[0], "document_embeddings": embeddings[1:]}
