# [SAME-SCENARIO] embed_text.py
# Generates an embedding vector for one text string

# Identifiable provider: OpenAI (OpenAI Embeddings)
import os
import openai

# Configure the OpenAI client using environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")


def embed_text(text: str) -> list[float]:
    """Return a single embedding vector (list of floats) for the given text.

    Uses OpenAI's text-embedding-ada-002 model via the OpenAI SDK.
    """
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text,
    )
    # response['data'][0]['embedding'] is a list of floats
    return response["data"][0]["embedding"]
