import numpy as np
from embedder_client import EmbedderClient  # local helper


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors.

    Uses NumPy for vector math.
    """
    a = np.array(vec_a)
    b = np.array(vec_b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def score_embeddings(query_text: str, corpus_texts: list[str]) -> list[float]:
    """Embed a query and a list of corpus texts, then compute similarity scores.

    Returns a list of similarity scores between the query embedding and each corpus embedding.
    """
    client = EmbedderClient()
    client.set_provider("openai")
    query_emb = client.embed(query_text)
    corpus_embs = client.embed_batch(corpus_texts)
    scores = [cosine_similarity(query_emb, cb) for cb in corpus_embs]
    return scores
