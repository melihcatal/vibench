from embeddings_client import EmbeddingsClient


def embed_batch(texts: list[str]) -> list[list[float]]:
    """
    Generates embeddings for a batch of texts.
    """
    client = EmbeddingsClient()
    return client.embed_batch(texts)


if __name__ == "__main__":
    sample_texts = ["Hello world", "How are you?", "This is a test sentence."]
    embeddings = embed_batch(sample_texts)
    for i, emb in enumerate(embeddings):
        print(
            f"Embedding for '{sample_texts[i]}': {emb[:5]}..."
        )  # Print first 5 elements
        print(f"Embedding length: {len(emb)}")
