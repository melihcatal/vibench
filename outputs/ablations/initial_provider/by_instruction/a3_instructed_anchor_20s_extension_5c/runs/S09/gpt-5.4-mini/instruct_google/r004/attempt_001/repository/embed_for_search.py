from typing import Dict, List

from embed_batch import embed_batch
from embed_text import embed_text


def embed_for_search(query: str, documents: List[str]) -> Dict[str, object]:
    query_embedding = embed_text(query).embedding
    document_embeddings = embed_batch(documents)
    return {"query": query_embedding, "documents": [item.embedding for item in document_embeddings]}
