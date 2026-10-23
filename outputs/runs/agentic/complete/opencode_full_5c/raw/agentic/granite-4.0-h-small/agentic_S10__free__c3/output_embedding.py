import json
from model_client import ModelClient
import uuid


def embed_output(text: str, model_name: str = "gpt-4o-mini") -> dict:
    """Generate an embedding for the provided text using a hosted LLM/text-embedding API.

    Args:
        text (str): The input string to embed.
        model_name (str): Hosted model identifier (default: gpt-4o-mini).

    Returns:
        dict: Contains the embedding (list of floats) and a unique identifier.
    """
    client = ModelClient(model_name)
    # Use the model's embedding endpoint (placeholder for actual API).
    embedding_response = client.complete(
        f"Provide a 1536-dimensional embedding (as comma-separated values) for the following text:\n\n{text}"
    )
    vec_str = embedding_response["text"].strip()
    embedding = [float(x) for x in vec_str.split(",")]
    return {
        "embedding_id": str(uuid.uuid4()),
        "embedding": embedding,
        "metadata": {"source": model_name},
    }
