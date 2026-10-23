from embeddings_client import EmbeddingsClient
from embeddings_models import cosine_similarity

client = EmbeddingsClient()


def compute_similarity(text1: str, text2: str) -> float:
    embedding1 = client.generate_embedding(text1)
    embedding2 = client.generate_embedding(text2)
    return cosine_similarity(embedding1, embedding2)
