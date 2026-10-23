import numpy as np
from typing import List

def similarity_score(embedding1: List[float], embedding2: List[float]) -> float:
    """Computes the cosine similarity between two embedding vectors."""
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0 # Handle case where one or both embeddings are zero vectors

    return dot_product / (norm_vec1 * norm_vec2)

if __name__ == '__main__':
    # Example usage (you would get these from an embedding API like in embed_text.py)
    # Using dummy embeddings for demonstration
    embedding_a = [0.1, 0.2, 0.3, 0.4]
    embedding_b = [0.1, 0.2, 0.3, 0.4] # Identical
    embedding_c = [0.5, 0.6, 0.7, 0.8] # Different

    score_ab = similarity_score(embedding_a, embedding_b)
    score_ac = similarity_score(embedding_a, embedding_c)

    print(f"Similarity between A and B (identical): {score_ab}")
    print(f"Similarity between A and C (different): {score_ac}")

    # Example with actual embedding generation (requires GOOGLE_API_KEY set)
    try:
        from embed_text import embed_text
        text1 = "apple"
        text2 = "fruit"
        text3 = "car"
        emb1 = embed_text(text1)
        emb2 = embed_text(text2)
        emb3 = embed_text(text3)
        print(f"Similarity (apple, fruit): {similarity_score(emb1, emb2)}")
        print(f"Similarity (apple, car): {similarity_score(emb1, emb3)}")
    except ImportError:
        print("Install google-generativeai and set GOOGLE_API_KEY to run live examples.")
    except Exception as e:
        print(f"Error running live examples: {e}")
