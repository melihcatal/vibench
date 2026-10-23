from __future__ import annotations

from dataclasses import asdict

from embed_text import embed_text
from embeddings_models import SearchBundle, SearchDocument, cosine_similarity


def embed_for_search(query: str, documents: list[dict[str, str]]) -> dict[str, object]:
    query_embedding = embed_text(query).embedding
    doc_models: list[SearchDocument] = []
    for document in documents:
        text = document["text"]
        embedding = embed_text(text).embedding
        doc_models.append(SearchDocument(id=document["id"], text=text, embedding=embedding))
    bundle = SearchBundle(query=query, query_embedding=query_embedding, documents=doc_models)
    ranked = sorted(
        (
            {"id": doc.id, "text": doc.text, "score": cosine_similarity(bundle.query_embedding, doc.embedding)}
            for doc in bundle.documents
        ),
        key=lambda item: item["score"],
        reverse=True,
    )
    return {"query": bundle.query, "query_embedding": bundle.query_embedding, "ranked_documents": ranked, "documents": [asdict(doc) for doc in bundle.documents]}
