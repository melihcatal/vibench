import os
from openai import OpenAI

from embeddings_client import get_embeddings_client


def generate_spoken_brief(search_results, config=None):
    config = config or {}
    client = get_embeddings_client(config)
    response = client.text_to_speech.create(input=search_results, voice='alloy')
    return {'audio_brief': response.audio_url}