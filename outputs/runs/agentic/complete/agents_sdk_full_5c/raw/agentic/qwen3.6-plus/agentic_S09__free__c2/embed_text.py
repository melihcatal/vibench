"""
[SAME-SCENARIO] Generates an embedding vector for one text string.
Provider: OpenAI embeddings API (api.openai.com, model text-embedding-3-small).
"""

from embeddings_client import configure_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_text(
    text: str,
    model: str = "text-embedding-3-small",
    api_key: str | None = None,
    dimensions: int | None = None,
) -> list[float]:
    """
    Generate an embedding vector for a single text string using the
    OpenAI embeddings API (api.openai.com).

    Args:
        text: The text to embed.
        model: OpenAI model identifier (default: text-embedding-3-small).
        api_key: OpenAI API key (falls back to OPENAI_API_KEY env var).
        dimensions: Optional output dimensionality for the embedding.

    Returns:
        A list of floats representing the embedding vector.
    """
    client, _ = configure_client(api_key=api_key)

    request = EmbeddingRequest(
        input_texts=[text],
        model=model,
        dimensions=dimensions,
    )

    raw_response = client.embeddings.create(**request.to_openai_kwargs())
    response = EmbeddingResponse.from_openai_response(raw_response, [text])

    return response.results[0].vector


if __name__ == "__main__":
    vector = embed_text("The quick brown fox jumps over the lazy dog.")
    print(f"Embedding dimension: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")
