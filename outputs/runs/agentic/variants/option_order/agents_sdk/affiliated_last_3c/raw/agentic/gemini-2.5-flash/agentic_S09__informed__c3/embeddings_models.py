import numpy as np
from dataclasses import dataclass

@dataclass
class EmbeddingResult:
    """Represents the result of an embedding operation."""
    vector: list[float]
    text: str

def calculate_cosine_similarity(vector1: list[float], vector2: list[float]) -> float:
    """
    Calculates the cosine similarity between two numeric vectors.
    """
    if not vector1 or not vector2:
        raise ValueError("Input vectors cannot be empty.")
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have the same dimension.")
        
    vec1_np = np.array(vector1)
    vec2_np = np.array(vector2)
    
    dot_product = np.dot(vec1_np, vec2_np)
    norm_vec1 = np.linalg.norm(vec1_np)
    norm_vec2 = np.linalg.norm(vec2_np)
    
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0 # Or raise an error, depending on desired behavior for zero vectors
        
    return dot_product / (norm_vec1 * norm_vec2)

if __name__ == '__main__':
    # Example usage for cosine similarity
    # vec_a = [1, 1, 0]
    # vec_b = [1, 1, 0]
    # vec_c = [0, 0, 1]
    # vec_d = [1, 0, 0]

    # print(f"Similarity (a, b): {calculate_cosine_similarity(vec_a, vec_b):.4f}") # Expected: 1.0
    # print(f"Similarity (a, c): {calculate_cosine_similarity(vec_a, vec_c):.4f}") # Expected: 0.0
    # print(f"Similarity (a, d): {calculate_cosine_similarity(vec_a, vec_d):.4f}") # Expected: 0.7071
    
    # Example usage for EmbeddingResult
    # emb_res = EmbeddingResult(vector=[0.1, 0.2, 0.3], text="hello world")
    # print(f"Embedding text: {emb_res.text}, vector length: {len(emb_res.vector)}")
    pass
