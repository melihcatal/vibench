import os

from embeddings_client import DirectEmbeddingsClient


def check_corpus_text(text: str) -> bool:
    client = DirectEmbeddingsClient()
    response = client.check_text(text)
    return response.is_safe
