import numpy as np
from typing import List

def similarity_score(embedding1: List[float], embedding2: List[float]) -> float:
    """Computes the cosine similarity between two embedding vectors.

    Args:
        embedding1: The first embedding vector.
        embedding2: The second embedding vector.

    Returns:
        A float representing the cosine similarity score.
    """
    # Ensure the embeddings are numpy arrays for efficient computation
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    # Compute dot product
    dot_product = np.dot(vec1, vec2)

    # Compute magnitudes
    magnitude1 = np.linalg.norm(vec1)
    magnitude2 = np.linalg.norm(vec2)

    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)

if __name__ == '__main__':
    # Example usage (for testing, not part of final submission requirements)
    # from embed_text import embed_text
    # from dotenv import load_dotenv
    # load_dotenv()

    # text1 = "apple"
    # text2 = "fruit"
    # text3 = "car"

    # emb1 = embed_text(text1)
    # emb2 = embed_text(text2)
    # emb3 = embed_text(text3)

    # print(f"Similarity('{text1}', '{text2}'): {similarity_score(emb1, emb2)}")
    # print(f"Similarity('{text1}', '{text3}'): {similarity_score(emb1, emb3)}")
    pass
