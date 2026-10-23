import os

from embeddings_client import DirectEmbeddingsClient


def similarity_score(text1: str, text2: str) -> float:
    client = DirectEmbeddingsClient()
    embedding1 = client.embed_text(text1).embeddings[0]
    embedding2 = client.embed_text(text2).embeddings[0]
    similarity = DirectEmbeddingsClient.cosine_similarity(embedding1, embedding2)
    return similarity
