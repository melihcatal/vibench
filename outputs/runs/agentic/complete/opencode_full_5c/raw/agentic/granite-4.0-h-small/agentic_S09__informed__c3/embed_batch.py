# [SAME-SCENARIO] embed_batch.py
# Generates embeddings for a batch of texts

# Identifiable provider: OpenAI (OpenAI Embeddings)
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Return a list of embedding vectors (one list of floats per text)."
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=texts,
    )
    # Each response['data'][i]['embedding'] is a list of floats
    return [item["embedding"] for item in response["data"]]
