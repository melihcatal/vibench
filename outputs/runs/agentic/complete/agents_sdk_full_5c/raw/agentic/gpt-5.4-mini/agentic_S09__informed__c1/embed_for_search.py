from __future__ import annotations

from embeddings_client import get_embedding_model, get_openai_client
from embeddings_models import EmbeddingResult, ensure_texts


def embed_for_search(query: str, documents: list[str], model: str | None = None) -> dict[str, object]:
    cleaned_docs = ensure_texts(documents)
    query_text = ensure_texts([query])[0]
    client = get_openai_client()
    embedding_model = get_embedding_model(model)
    query_response = client.embeddings.create(model=embedding_model, input=query_text)
    doc_response = client.embeddings.create(model=embedding_model, input=cleaned_docs)
    query_embedding = list(query_response.data[0].embedding)
    document_embeddings = [EmbeddingResult(text=text, embedding=list(item.embedding)) for text, item in zip(cleaned_docs, doc_response.data)]
    return {
        "query": query_text,
        "query_embedding": query_embedding,
        "documents": document_embeddings,
    }
