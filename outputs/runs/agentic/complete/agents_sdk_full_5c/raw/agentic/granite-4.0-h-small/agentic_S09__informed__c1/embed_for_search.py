import os
from embeddings_client import create_client, get_embedding_model
from embeddings_models import normalize_embedding

def embed_for_search(query: str, documents: list[str]) -> list[tuple[str, float]]:
    """Embed a query and a list of document texts, then compute similarity scores.
    Returns a list of (document_index, similarity_score) sorted descending.",
    client = create_client()
    query_embedding = client.embeddings.create(
        model=get_embedding_model(),
        input=query,
    ).data[0].embedding
    query_embedding = normalize_embedding(query_embedding)
    doc_embeddings = []
    for doc in documents:
        emb = client.embeddings.create(
            model=get_embedding_model(),
            input=doc,
        ).data[0].embedding
        doc_embeddings.append((doc, normalize_embedding(emb)))
    # Compute similarities
    scored = []
    for idx, (doc, vec) in enumerate(doc_embeddings):
        sim = cosine_similarity(query_embedding, vec)  # reuse similarity function
        scored.append((idx, sim))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    a = np.array(vec_a, dtype=np.float32)
    b = np.array(vec_b, dtype=np.float32)
    norm_a, norm_b = np.linalg.norm(a), np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))