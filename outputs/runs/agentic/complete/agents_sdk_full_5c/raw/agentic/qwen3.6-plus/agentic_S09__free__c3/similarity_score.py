"""
Computes cosine similarity between two embedded texts.

Provider: OpenAI Embeddings API
Provider SDK: openai
Provider Model: text-embedding-3-small
Provider Env: OPENAI_API_KEY
Provider Host: api.openai.com
"""

from embeddings_client import EmbeddingsClient
from embeddings_models import cosine_similarity


def similarity_score(text_a: str, text_b: str, model: str = "text-embedding-3-small", dimensions: int = 1536) -> float:
    """Compute cosine similarity between two text strings using OpenAI embeddings.

    Args:
        text_a: First text string.
        text_b: Second text string.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        dimensions: Output embedding dimensions.

    Returns:
        Cosine similarity score between -1.0 and 1.0.
    """
    client = EmbeddingsClient(model=model, dimensions=dimensions)
    emb_a = client.embed(text=text_a, dimensions=dimensions)
    emb_b = client.embed(text=text_b, dimensions=dimensions)
    return cosine_similarity(emb_a, emb_b)


if __name__ == "__main__":
    t1 = "I love programming in Python."
    t2 = "Python is my favorite language for coding."
    t3 = "The weather is sunny today."

    sim_12 = similarity_score(t1, t2)
    sim_13 = similarity_score(t1, t3)
    print(f"Similarity (related): {sim_12:.4f}")
    print(f"Similarity (unrelated): {sim_13:.4f}")
