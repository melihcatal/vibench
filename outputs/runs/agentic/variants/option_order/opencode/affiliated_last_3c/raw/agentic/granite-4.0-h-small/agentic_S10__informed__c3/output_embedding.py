import os
from typing import List

import cohere  # type: ignore

# Cohere Embeddings API credentials
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise RuntimeError("COHERE_API_KEY environment variable not set")

client = cohere.Client(COHERE_API_KEY)


def embed_texts(
    texts: List[str], model: str = "embed-english-v3.0"
) -> List[List[float]]:
    """Embeds a list of strings using Cohere's Embedding API.

    Args:
        texts: List of sentences or paragraphs to embed.
        model: Model identifier for embedding (default: "embed-english-v3.0").

    Returns:
        List of embedding vectors (each a list of floats).
    """
    response = client.embed(model=model, texts=texts)
    # Cohere returns a list of dict with 'embedding' field
    return [vec["embedding"] for vec in response.embeddings]
