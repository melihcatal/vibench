from __future__ import annotations

from embeddings_client import get_embedding_model
from embeddings_models import SearchDocument, SearchResult, cosine_similarity
from embed_batch import embed_batch
from embed_text import embed_text


def embed_for_search(query: str, documents: list[SearchDocument], model: str | None = None) -> tuple[list[float], list[SearchResult]]:
    resolved_model = model or get_embedding_model()
    query_vector = embed_text(query, model=resolved_model).vector
    doc_texts = [document.text for document in documents]
    doc_embeddings = embed_batch(doc_texts, model=resolved_model).vectors
    results = [
        SearchResult(id=document.id, text=document.text, score=cosine_similarity(query_vector, doc_vector))
        for document, doc_vector in zip(documents, doc_embeddings)
    ]
    results.sort(key=lambda item: item.score, reverse=True)
    return query_vector, results
