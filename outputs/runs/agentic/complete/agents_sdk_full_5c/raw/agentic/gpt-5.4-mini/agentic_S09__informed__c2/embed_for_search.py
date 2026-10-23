from embed_batch import embed_batch
from embed_text import embed_text
from embeddings_models import cosine_similarity


SEARCH_PROVIDER = "OpenAI Embeddings API"


def embed_for_search(query: str, documents):
    query_vector = embed_text(query).vector
    doc_vectors = embed_batch(documents).vectors
    scored = []
    for document, vector in zip(documents, doc_vectors):
        scored.append((document, cosine_similarity(query_vector, vector)))
    scored.sort(key=lambda item: item[1], reverse=True)
    return {"query": query_vector, "ranked_documents": scored}
