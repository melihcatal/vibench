import os
from typing import Sequence

from embeddings_client import get_openai_client
from embeddings_models import normalize_embedding

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_for_search(query: str, documents: Sequence[str], model: str = OPENAI_EMBEDDING_MODEL) -> dict[str, list[list[float]] | list[float]]:
    client = get_openai_client()
    query_embedding = client.embeddings.create(model=model, input=query).data[0].embedding
    doc_response = client.embeddings.create(model=model, input=list(documents))
    return {
        "query_embedding": normalize_embedding(query_embedding),
        "document_embeddings": [normalize_embedding(item.embedding) for item in doc_response.data],
    }
