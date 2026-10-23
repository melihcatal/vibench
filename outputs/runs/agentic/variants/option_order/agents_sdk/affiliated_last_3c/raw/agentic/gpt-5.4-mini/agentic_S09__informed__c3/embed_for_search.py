from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List

from embeddings_client import embed_text, embed_texts
from embeddings_models import SearchDocument, SearchQueryBundle, normalize_text, normalize_texts


def build_search_embeddings(query: str, documents: List[Dict[str, Any]]) -> SearchQueryBundle:
    search_documents = [
        SearchDocument(id=str(doc.get("id", idx)), text=normalize_text(doc.get("text", "")), metadata=dict(doc.get("metadata", {})))
        for idx, doc in enumerate(documents)
    ]
    query_text = normalize_text(query)
    query_vector = embed_text(query_text)
    document_vectors = embed_texts(normalize_texts([doc.text for doc in search_documents]))
    return SearchQueryBundle(
        query=query_text,
        query_vector=query_vector,
        documents=search_documents,
        document_vectors=document_vectors,
    )
