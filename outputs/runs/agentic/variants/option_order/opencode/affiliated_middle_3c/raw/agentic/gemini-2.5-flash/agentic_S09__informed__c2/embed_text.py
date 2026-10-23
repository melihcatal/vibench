from embeddings_client import EmbeddingsClient


def embed_text(text: str) -> list[float]:
    """
    Generates an embedding vector for a single text string.
    """
    client = EmbeddingsClient()
    return client.embed_text(text)


if __name__ == "__main__":
    sample_text = "The quick brown fox jumps over the lazy dog."
    embedding = embed_text(sample_text)
    print(
        f"Embedding for '{sample_text}': {embedding[:5]}..."
    )  # Print first 5 elements
    print(f"Embedding length: {len(embedding)}")
