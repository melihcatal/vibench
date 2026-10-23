from __future__ import annotations

from typing import Sequence

from embeddings_client import DEFAULT_EMBEDDING_MODEL, create_embeddings
from embeddings_models import EmbeddingRecord, SearchEmbeddingSet


def embed_for_search(
    query: str,
    documents: Sequence[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: int | None = None,
) -> SearchEmbeddingSet:
    query_response = create_embeddings([query], model=model, dimensions=dimensions, input_type="search_query")
    document_response = create_embeddings(list(documents), model=model, dimensions=dimensions, input_type="search_document")
    query_record = EmbeddingRecord(index=0, embedding=query_response.records[0].embedding, text=query)
    document_records = [
        EmbeddingRecord(index=record.index, embedding=record.embedding, text=record.text)
        for record in document_response.records
    ]
    return SearchEmbeddingSet(query=query_record, documents=document_records, model=query_response.model)
