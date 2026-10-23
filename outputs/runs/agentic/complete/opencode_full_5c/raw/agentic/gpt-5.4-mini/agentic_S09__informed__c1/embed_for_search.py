from embed_batch import embed_batch
from embed_text import embed_text
from similarity_score import cosine_similarity


def embed_for_search(query: str, documents):
    query_vector = embed_text(query)
    document_vectors = embed_batch(documents)
    scores = [cosine_similarity(query, doc) for doc in documents]
    return {"query": query_vector, "documents": document_vectors, "scores": scores}
