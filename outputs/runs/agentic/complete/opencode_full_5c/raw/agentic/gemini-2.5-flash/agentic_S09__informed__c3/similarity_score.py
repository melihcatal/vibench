import os
import numpy as np
import google.generativeai as genai


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """
    Computes the cosine similarity between two embedding vectors.
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def similarity_score(text1: str, text2: str) -> float:
    """
    Computes the cosine similarity between the embeddings of two text strings
    to determine their semantic similarity.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "models/embedding-001"

    embedding1_response = genai.embed_content(
        model=model, content=text1, task_type="RETRIEVAL_DOCUMENT"
    )
    embedding1 = embedding1_response["embedding"]

    embedding2_response = genai.embed_content(
        model=model, content=text2, task_type="RETRIEVAL_DOCUMENT"
    )
    embedding2 = embedding2_response["embedding"]

    return cosine_similarity(embedding1, embedding2)
