import os
from openai import OpenAI

from embeddings_models import EmbeddingRequest, EmbeddingResponse
from embeddings_client import get_embeddings_client


def embed_batch(payload, config=None):
    client = get_embeddings_client(config)
    request = EmbeddingRequest(texts=payload['texts'])
    response = client.embeddings.create(model='text-embedding-3-small', input=request.texts)
    return EmbeddingResponse(embeddings=[item.embedding for item in response.data])