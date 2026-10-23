import os
from openai import OpenAI


def embed_output(text: str) -> list[float]:
    """Embed platform outputs for evaluation or retrieval using OpenAI Embeddings."""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002",  # Concrete model identifier for OpenAI embeddings
    )
    return response.data[0].embedding
