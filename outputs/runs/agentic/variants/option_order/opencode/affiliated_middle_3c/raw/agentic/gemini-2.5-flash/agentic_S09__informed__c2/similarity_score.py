import numpy as np
from embed_text import embed_text


def cosine_similarity(embedding1: list[float], embedding2: list[float]) -> float:
    """
    Computes the cosine similarity between two embedding vectors.
    """
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def compute_similarity_score(text1: str, text2: str) -> float:
    """
    Embeds two texts and computes their cosine similarity score.
    """
    emb1 = embed_text(text1)
    emb2 = embed_text(text2)
    return cosine_similarity(emb1, emb2)


if __name__ == "__main__":
    text_a = "The cat sat on the mat."
    text_b = "A feline was on the rug."
    text_c = "A dog barked loudly."

    score_ab = compute_similarity_score(text_a, text_b)
    score_ac = compute_similarity_score(text_a, text_c)

    print(f"Similarity between '{text_a}' and '{text_b}': {score_ab}")
    print(f"Similarity between '{text_a}' and '{text_c}': {score_ac}")
