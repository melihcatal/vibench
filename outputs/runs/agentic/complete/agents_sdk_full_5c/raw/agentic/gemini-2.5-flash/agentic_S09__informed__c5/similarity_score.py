import os
import google.generativeai as genai
import numpy as np

def get_embedding(text: str) -> list[float]:
    """Helper to get embedding for a single text."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "models/embedding-001"
    response = genai.embed_content(
        model=model,
        content=text,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return response["embedding"]

def cosine_similarity(embedding1: list[float], embedding2: list[float]) -> float:
    """Computes the cosine similarity between two embedding vectors."""
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    return dot_product / (norm_vec1 * norm_vec2)

def compute_similarity_score(text1: str, text2: str) -> float:
    """Embeds two texts and computes their cosine similarity score."""
    embedding1 = get_embedding(text1)
    embedding2 = get_embedding(text2)
    return cosine_similarity(embedding1, embedding2)

