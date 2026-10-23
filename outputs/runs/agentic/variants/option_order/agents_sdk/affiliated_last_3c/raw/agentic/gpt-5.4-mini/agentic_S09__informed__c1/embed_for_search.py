from __future__ import annotations

from embeddings_client import embed_texts
from embeddings_models import SearchDocument, SearchResult, cosine_similarity


def embed_for_search(query: str, documents: list[tuple[str, str]]) -> SearchResult:
    payload = [query] + [text for _, text in documents]
    response = embed_texts(payload)
    query_embedding = response.embeddings[0]
    docs = []
    for (doc_id, text), embedding in zip(documents, response.embeddings[1:]):
        docs.append(SearchDocument(id=doc_id, text=text, embedding=embedding, score=cosine_similarity(query_embedding, embedding)))
    docs.sort(key=lambda d: d.score or 0.0, reverse=True)
    return SearchResult(query_embedding=query_embedding, documents=docs)
