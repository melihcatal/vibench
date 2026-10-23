# [SAME-SCENARIO] embed_text.py
# Generates an embedding vector for one text string

# Provider: OpenAI Embeddings
# SDK: openai
# Integration signal: OPENAI_API_KEY environment variable

import os
from openai import OpenAI

embeddings_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_text(text: str) -> list[float]:
    """Return embedding vector for a single text string."""
    response = embeddings_client.embeddings.create(
        model="text-embedding-ada-002",
        input=text,
    )
    return response.data[0].embedding
