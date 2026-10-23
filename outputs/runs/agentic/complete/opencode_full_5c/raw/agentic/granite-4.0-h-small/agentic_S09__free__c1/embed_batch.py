# [SAME-SCENARIO] embed_batch.py
# Generates embeddings for a batch of text strings using OpenAI's embeddings API

import os
from openai import OpenAI
from embeddings_client import get_openai_client
from embeddings_models import EmbedBatchRequest, EmbedBatchResponse


def embed_batch(texts: list[str]) -> EmbedBatchResponse:
    """Embed a batch of text strings and return a list of embedding vectors.

    Uses the OpenAI embeddings endpoint.
    """
    client = get_openai_client()
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=texts,
    )
    # Each element in response.data is an embedding object
    embeddings = [item.embedding for item in response.data]
    return EmbedBatchResponse(embeddings=embeddings, model="text-embedding-3-large")
