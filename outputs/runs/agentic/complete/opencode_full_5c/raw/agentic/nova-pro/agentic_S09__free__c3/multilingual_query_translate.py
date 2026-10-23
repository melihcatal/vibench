import os

from embeddings_client import DirectEmbeddingsClient


def translate_query(query: str, target_language: str) -> str:
    client = DirectEmbeddingsClient()
    response = client.translate_text(query, target_language)
    return response.translated_text
