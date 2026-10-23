from embed_text import generate_embedding
from embeddings_models import cosine_similarity


def calculate_similarity(
    text1: str, text2: str, model: str = "text-embedding-3-small"
) -> float:
    """
    Computes cosine similarity between two embedded texts using OpenAI embeddings.
    """
    embedding1_response = generate_embedding(text1, model)
    embedding2_response = generate_embedding(text2, model)

    return cosine_similarity(
        embedding1_response.embedding, embedding2_response.embedding
    )
