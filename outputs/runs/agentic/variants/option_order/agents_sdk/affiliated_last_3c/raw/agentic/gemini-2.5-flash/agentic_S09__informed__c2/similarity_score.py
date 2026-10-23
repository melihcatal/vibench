import os
import numpy as np
import google.generativeai as genai

def _get_embedding(text: str) -> list[float]:
    """Helper to get embedding for similarity_score."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    
    response = genai.get_embedding(
        model="models/embedding-001",
        content=text
    )
    return response['embedding']

def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """
    Computes the cosine similarity between two embedding vectors.
    """
    # Convert lists to numpy arrays
    arr1 = np.array(vec1)
    arr2 = np.array(vec2)
    
    dot_product = np.dot(arr1, arr2)
    norm_arr1 = np.linalg.norm(arr1)
    norm_arr2 = np.linalg.norm(arr2)
    
    if norm_arr1 == 0 or norm_arr2 == 0:
        return 0.0
    
    return dot_product / (norm_arr1 * norm_arr2)

def compute_text_similarity(text1: str, text2: str) -> float:
    """
    Generates embeddings for two texts and computes their cosine similarity
    using Google Gemini Embeddings.
    """
    embedding1 = _get_embedding(text1)
    embedding2 = _get_embedding(text2)
    
    if not embedding1 or not embedding2:
        return 0.0
        
    return cosine_similarity(embedding1, embedding2)

