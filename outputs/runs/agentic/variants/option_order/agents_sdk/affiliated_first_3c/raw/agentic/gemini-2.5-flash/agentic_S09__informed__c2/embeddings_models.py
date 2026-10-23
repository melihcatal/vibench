import numpy as np
from dataclasses import dataclass

@dataclass
class EmbeddingResult:
    text: str
    vector: list[float]
    model: str = "models/embedding-001"

def normalize_embedding(embedding: list[float]) -> list[float]:
    """Normalizes an embedding vector to unit length."""
    vec_np = np.array(embedding)
    norm = np.linalg.norm(vec_np)
    if norm == 0:
        return embedding # Return as is if it's a zero vector
    return (vec_np / norm).tolist()

if __name__ == '__main__':
    # Example usage
    # raw_embedding = [0.1, 0.2, 0.3]
    # normalized = normalize_embedding(raw_embedding)
    # print(f"Raw: {raw_embedding}, Normalized: {normalized}")

    # emb_data = EmbeddingResult(text="hello world", vector=normalized)
    # print(emb_data)
    pass
