import numpy as np
from embed_text import generate_embedding


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Computes cosine similarity between the embeddings of two texts.
    """
    embedding1 = generate_embedding(text1)
    embedding2 = generate_embedding(text2)

    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    cosine_similarity = np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )

    return float(cosine_similarity)


if __name__ == "__main__":
    # This is an example and will not be executed
    text_a = "The cat sat on the mat."
    text_b = "A feline was resting on the rug."
    text_c = "The weather is sunny today."

    similarity_ab = calculate_similarity(text_a, text_b)
    similarity_ac = calculate_similarity(text_a, text_c)

    print(f"Similarity between A and B: {similarity_ab}")
    print(f"Similarity between A and C: {similarity_ac}")
