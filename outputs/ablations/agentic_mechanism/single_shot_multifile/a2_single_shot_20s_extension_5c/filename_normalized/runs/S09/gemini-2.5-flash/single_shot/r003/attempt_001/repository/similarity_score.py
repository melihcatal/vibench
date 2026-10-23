import os
import math
import google.generativeai as genai

def _normalize_vector(vector: list[float]) -> list[float]:
    """Normalizes a vector to unit length."""
    norm = math.sqrt(sum(x*x for x in vector))
    if norm == 0:
        return [0.0] * len(vector)
    return [x / norm for x in vector]

def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    """Computes the cosine similarity between two vectors."""
    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must be of the same length")
    
    # Normalize vectors
    norm_a = _normalize_vector(vector_a)
    norm_b = _normalize_vector(vector_b)
    
    dot_product = sum(a * b for a, b in zip(norm_a, norm_b))
    return dot_product

def get_embedding_and_compare(text1: str, text2: str) -> float:
    """Generates embeddings for two texts and computes their cosine similarity using Google Generative AI.
    Returns the cosine similarity score."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model_name = "models/embedding-001"

    # Embed texts
    embedding1_response = genai.embed_content(model=model_name, content=text1)
    embedding2_response = genai.embed_content(model=model_name, content=text2)
    
    vector1 = embedding1_response["embedding"]
    vector2 = embedding2_response["embedding"]
    
    return cosine_similarity(vector1, vector2)