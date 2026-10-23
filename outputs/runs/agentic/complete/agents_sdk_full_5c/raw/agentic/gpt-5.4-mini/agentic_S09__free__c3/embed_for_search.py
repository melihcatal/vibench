from __future__ import annotations

from embeddings_client import get_client, load_settings
from embeddings_models import SearchDocument, SearchResult, cosine_similarity, normalize_texts, normalize_vector


def embed_for_search(query: str, documents: list[SearchDocument]) -> list[SearchResult]:
    settings = load_settings()
    client = get_client(settings)
    query_clean = normalize_texts([query])[0]
    query_embedding = normalize_vector(
        client.embeddings.create(model=settings.embedding_model, input=query_clean).data[0].embedding
    )

    doc_texts = normalize_texts([doc.text for doc in documents])
    doc_embeddings = client.embeddings.create(model=settings.embedding_model, input=doc_texts).data

    results: list[SearchResult] = []
    for doc, emb in zip(documents, doc_embeddings):
        score = cosine_similarity(query_embedding, normalize_vector(emb.embedding))
        results.append(SearchResult(doc_id=doc.doc_id, score=score, text=doc.text))
    return sorted(results, key=lambda r: r.score, reverse=True)
