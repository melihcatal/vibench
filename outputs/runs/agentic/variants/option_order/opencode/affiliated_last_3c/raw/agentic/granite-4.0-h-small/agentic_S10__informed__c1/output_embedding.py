# Embed model outputs for clustering or retrieval using Anthropic Embeddings via Anthropic SDK
import anthropic


def embed_text(text: str, model: str = "embedding-ada-001") -> list:
    """Obtain embedding vector for a given text.

    Args:
        text: Input text to embed.
        model: Model identifier for Anthropic embedding endpoint.

    Returns:
        List of float values representing the embedding.
    """
    client = anthropic.Anthropic(api_key="ANTHROPIC_API_KEY")
    embedding = client.embeddings.create(model=model, input=text)
    # Anthropic returns a dict with 'embedding' field
    return embedding["embedding"]
