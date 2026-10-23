import os
from typing import List
from openai import OpenAI


def initialize_openai_client() -> OpenAI:
    """Initialize the OpenAI client with API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    return OpenAI(api_key=api_key)


def embed_script(script: str, model: str = "text-embedding-3-small") -> List[float]:
    """Embed narration scripts for voice-asset search using OpenAI Embeddings."""
    client = initialize_openai_client()

    response = client.embeddings.create(input=script, model=model)

    return response.data[0].embedding


def batch_embed_scripts(
    scripts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """Embed a batch of narration scripts using OpenAI Embeddings."""
    client = initialize_openai_client()

    response = client.embeddings.create(input=scripts, model=model)

    return [data.embedding for data in response.data]
