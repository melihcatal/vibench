import os

from google import genai

from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding_response


def embed_batch(payload, config=None):
    client = get_embeddings_client(config)
    responses = client.models.embed_content(model="gemini-embedding-001", contents=payload["texts"])
    return [normalize_embedding_response(response) for response in responses]