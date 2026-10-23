import os
from openai import OpenAI

from embeddings_models import EmbeddingResponse
from embeddings_client import get_embeddings_client


def retrieval_audio_brief(search_results, config=None):
    client = get_embeddings_client(config)
    audio_response = client.audio.create(model='tts-1', input=' '.join(search_results))
    return {'audio_brief': audio_response.url}