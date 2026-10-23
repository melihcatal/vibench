from typing import List, Dict, Tuple

from embed_batch import embed_batch


def embed_for_search(query: str, documents: List[str]) -> Dict[str, List[float]]:
    """Embed a query and documents for semantic search using IBM Slate Embeddings."""
    texts = [query] + documents
    embeddings = embed_batch(texts)
    return {"query_embedding": embeddings[0], "document_embeddings": embeddings[1:]}


def search_documents(
    query: str, documents: List[str], top_k: int = 3
) -> List[Tuple[str, float]]:
    """Perform semantic search and return top-k documents with similarity scores."""
    from similarity_score import similarity_score

    embedded = embed_for_search(query, documents)
    query_embedding = embedded["query_embedding"]
    doc_embeddings = embedded["document_embeddings"]

    scores = []
    for doc, doc_embedding in zip(documents, doc_embeddings):
        score = similarity_score(query, doc)  # Reuses cosine_similarity internally
        scores.append((doc, score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]
