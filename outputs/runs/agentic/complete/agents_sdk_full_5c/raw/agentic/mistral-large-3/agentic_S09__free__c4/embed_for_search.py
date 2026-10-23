from typing import List, Dict, Any
from embed_batch import embed_batch

def embed_for_search(query: str, documents: List[str]) -> Dict[str, Any]:
    texts = [query] + documents
    embeddings = embed_batch(texts)
    query_embedding = embeddings[0]
    document_embeddings = embeddings[1:]
    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
        "documents": documents
    }