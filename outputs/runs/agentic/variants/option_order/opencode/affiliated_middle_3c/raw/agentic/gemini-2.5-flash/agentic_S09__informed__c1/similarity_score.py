from embed_text import embed_text
from embeddings_models import calculate_cosine_similarity


def get_similarity_score(
    text1: str, text2: str, model_name: str = "models/embedding-001"
) -> float:
    """Computes the cosine similarity between two embedded texts using Google Gemini Embeddings.

    Args:
        text1: The first text string.
        text2: The second text string.
        model_name: The name of the embedding model to use. Default is "models/embedding-001".

    Returns:
        A float representing the cosine similarity score.
    """
    embedding1 = embed_text(text1, model_name)
    embedding2 = embed_text(text2, model_name)
    return calculate_cosine_similarity(embedding1, embedding2)
