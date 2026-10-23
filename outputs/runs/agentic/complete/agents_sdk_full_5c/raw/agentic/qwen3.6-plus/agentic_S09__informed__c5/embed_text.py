"""
[SAME-SCENARIO] Generates an embedding vector for one text string.
Provider: OpenAI Embeddings API (text-embedding-3-small)
SDK: openai
Auth: OPENAI_API_KEY
"""

from typing import List, Optional

from embeddings_client import get_openai_client, get_embedding_model
from embeddings_models import normalize_vector, build_embedding_request


def embed_text(
    text: str,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    normalize: bool = True,
    dimensions: Optional[int] = None,
) -> List[float]:
    """
    Generate an embedding vector for a single text string using OpenAI.

    Args:
        text: The input text to embed.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        api_key: Optional OpenAI API key (falls back to OPENAI_API_KEY env var).
        normalize: Whether to L2-normalize the returned vector.
        dimensions: Optional output dimensionality for the embedding.

    Returns:
        A list of floats representing the embedding vector.
    """
    client = get_openai_client(api_key=api_key)
    model_name = model or get_embedding_model()

    request = build_embedding_request(
        texts=[text],
        model=model_name,
        dimensions=dimensions,
    )

    response = client.embeddings.create(
        model=request.model,
        input=request.input_texts[0],
        encoding_format="float",
        dimensions=dimensions,
    )

    vector = response.data[0].embedding

    if normalize:
        vector = normalize_vector(vector)

    return vector


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = "The quick brown fox jumps over the lazy dog."
    vec = embed_text(query)
    print(f"Embedding dimension: {len(vec)}")
    print(f"First 5 values: {vec[:5]}")
