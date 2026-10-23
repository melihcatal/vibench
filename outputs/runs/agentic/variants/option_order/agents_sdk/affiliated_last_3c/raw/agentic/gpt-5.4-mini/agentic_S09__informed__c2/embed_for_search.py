from dataclasses import dataclass
from typing import List

from embed_batch import embed_batch
from embed_text import embed_text


@dataclass
class SearchEmbeddingPack:
    query_vector: List[float]
    document_vectors: List[List[float]]
    model: str


def embed_for_search(query: str, documents):
    query_embedding = embed_text(query)
    docs_embedding = embed_batch(documents)
    return SearchEmbeddingPack(
        query_vector=query_embedding.vector,
        document_vectors=docs_embedding.vectors,
        model=query_embedding.model,
    )
