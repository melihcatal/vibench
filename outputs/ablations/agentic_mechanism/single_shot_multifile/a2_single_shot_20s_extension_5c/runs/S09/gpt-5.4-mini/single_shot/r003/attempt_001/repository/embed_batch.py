import os
from typing import List, Sequence

from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding_response

MODEL_ID = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_batch(texts: List[str]) -> List[Sequence[float]]:
    client = get_embeddings_client()
    response = client.embeddings.create(model=MODEL_ID, input=texts)
    return normalize_embedding_response(response)
