# [SAME-SCENARIO] embed_text.py
# Generates an embedding vector for one text string using OpenAI Embeddings API

import os
import openai

# Load API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")


def embed_text(text: str) -> list[float]:
    """Return a list of floats representing the embedding of the input text.

    Args:
        text (str): The text to embed.

    Returns:
        list[float]: Embedding vector.
    """
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text,
    )
    # response['data'][0]['embedding'] is a list of floats
    return response["data"][0]["embedding"]
