from __future__ import annotations

from collections.abc import Sequence

from embeddings_client import CohereEmbeddingsClient
from embeddings_models import SearchEmbeddingBundle, ensure_texts


def prepare_search_embeddings(query: str, documents: Sequence[str]) -> SearchEmbeddingBundle:
    client = CohereEmbeddingsClient()
    clean_documents = ensure_texts(documents)
    query_result = client.embed_texts(query, input_type="search_query")
    document_result = client.embed_texts(clean_documents, input_type="search_document")
    return SearchEmbeddingBundle(
        query_embedding=query_result.embeddings[0],
        document_embeddings=document_result.embeddings,
        documents=clean_documents,
        model=document_result.model,
    )
