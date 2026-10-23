# [SAME-SCENARIO] embed_text.py
# Generates an embedding vector for a single text string using OpenAI's embeddings API

import os
from openai import OpenAI
from embeddings_client import get_openai_client
from embeddings_models import EmbedRequest, EmbedResponse


def embed_text(text: str) -> EmbedResponse:
    """Embed a single text string and return the embedding vector.

    Uses the OpenAI embeddings endpoint.
    """
    client = get_openai_client()
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text,
    )
    # The API returns a list with one embedding object
    embedding = response.data[0].embedding
    return EmbedResponse(embedding=embedding, model="text-embedding-3-large")
