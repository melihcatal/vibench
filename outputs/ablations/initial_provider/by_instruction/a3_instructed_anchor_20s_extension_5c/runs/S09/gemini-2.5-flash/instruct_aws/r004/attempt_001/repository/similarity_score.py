from embeddings_models import cosine_similarity
from embed_text import embed_text

def get_similarity_score(text1: str, text2: str) -> float:
    """
    Computes the cosine similarity between two text strings after embedding them 
    using AWS Bedrock.
    """
    embedding1 = embed_text(text1)
    embedding2 = embed_text(text2)

    score = cosine_similarity(embedding1, embedding2)
    return score
