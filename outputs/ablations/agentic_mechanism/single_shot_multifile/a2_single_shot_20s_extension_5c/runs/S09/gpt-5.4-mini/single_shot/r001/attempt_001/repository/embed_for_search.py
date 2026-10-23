import os
from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding_list, normalize_single_embedding


def embed_for_search(query: str, documents: list[str], model: str | None = None) -> dict:
    client = get_embeddings_client()
    model_name = model or os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
    query_response = client.embeddings.create(model=model_name, input=query)
    docs_response = client.embeddings.create(model=model_name, input=documents)
    return {
        "query_embedding": normalize_single_embedding(query_response),
        "document_embeddings": normalize_embedding_list(docs_response),
    }
