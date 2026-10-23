import os
import google.generativeai as genai
import numpy as np

def _get_embedding(text: str) -> list[float]:
    """Helper to get an embedding for a single text."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('models/embedding-001')
    response = model.embed_content(
        content=text,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return response['embedding']

def cosine_similarity(embedding1: list[float], embedding2: list[float]) -> float:
    """
    Computes the cosine similarity between two embedding vectors.
    """
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    return dot_product / (norm_vec1 * norm_vec2)

def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    Generates embeddings for two texts and computes their cosine similarity.
    """
    embedding1 = _get_embedding(text1)
    embedding2 = _get_embedding(text2)
    return cosine_similarity(embedding1, embedding2)

if __name__ == '__main__':
    text_a = "The cat sat on the mat."
    text_b = "A feline rested on the rug."
    text_c = "The sky is blue."

    similarity_ab = calculate_text_similarity(text_a, text_b)
    similarity_ac = calculate_text_similarity(text_a, text_c)

    print(f"Similarity between '{text_a}' and '{text_b}': {similarity_ab:.4f}")
    print(f"Similarity between '{text_a}' and '{text_c}': {similarity_ac:.4f}")
