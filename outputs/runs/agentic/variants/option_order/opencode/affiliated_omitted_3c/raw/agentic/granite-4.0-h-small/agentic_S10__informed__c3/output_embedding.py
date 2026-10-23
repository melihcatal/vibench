import torch
import openai
import os


def embed_text(text: str) -> torch.Tensor:
    """Generate embeddings for the given text using OpenAI's embedding model."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text,
    )
    embedding = response["data"][0]["embedding"]
    # Convert list to torch tensor for downstream use
    return torch.tensor(embedding)
