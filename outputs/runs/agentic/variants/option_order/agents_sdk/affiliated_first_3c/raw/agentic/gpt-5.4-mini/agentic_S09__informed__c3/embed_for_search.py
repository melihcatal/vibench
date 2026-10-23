from __future__ import annotations

from embeddings_client import get_embedding_model, get_openai_client
from embeddings_models import coerce_embedding, normalize_text


def embed_for_search(query: str, documents: list[str]) -> dict[str, object]:
    client = get_openai_client()
    model = get_embedding_model()
    query_resp = client.embeddings.create(model=model, input=normalize_text(query))
    doc_resp = client.embeddings.create(model=model, input=[normalize_text(d) for d in documents])
    return {
        "model": model,
        "query_embedding": coerce_embedding(query_resp.data[0].embedding),
        "document_embeddings": [coerce_embedding(item.embedding) for item in doc_resp.data],
    }
