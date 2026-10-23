from typing import List, Dict, Tuple
from embed_batch import embed_batch

def embed_for_search(query: str, documents: List[str]) -> Tuple[List[float], List[Dict]]:
    texts = [query] + documents
    embeddings = embed_batch(texts)
    query_embedding = embeddings[0]
    document_embeddings = [
        {"text": doc, "embedding": emb}
        for doc, emb in zip(documents, embeddings[1:])
    ]
    return query_embedding, document_embeddings