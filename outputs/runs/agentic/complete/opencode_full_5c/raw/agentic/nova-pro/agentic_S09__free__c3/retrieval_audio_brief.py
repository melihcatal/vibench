import os

from embeddings_client import DirectEmbeddingsClient


def generate_spoken_brief(search_results: list) -> str:
    client = DirectEmbeddingsClient()
    response = client.generate_audio_brief(search_results)
    return response.audio_url
