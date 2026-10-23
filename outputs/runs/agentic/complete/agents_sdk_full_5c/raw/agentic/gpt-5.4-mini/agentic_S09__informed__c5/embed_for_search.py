from __future__ import annotations

from embeddings_client import get_client, get_model_name
from embeddings_models import SearchDocument


def embed_for_search(query: str, documents: list[dict[str, str]], model: str | None = None) -> dict[str, object]:
    chosen_model = get_model_name(model)
    client = get_client()
    query_embedding = list(client.embeddings.create(model=chosen_model, input=query).data[0].embedding)

    doc_texts = [doc["text"] for doc in documents]
    doc_result = client.embeddings.create(model=chosen_model, input=doc_texts)
    embedded_docs = [
        SearchDocument(doc_id=documents[i]["id"], text=documents[i]["text"], embedding=list(item.embedding))
        for i, item in enumerate(doc_result.data)
    ]
    return {"query_embedding": query_embedding, "documents": embedded_docs, "model": chosen_model}
