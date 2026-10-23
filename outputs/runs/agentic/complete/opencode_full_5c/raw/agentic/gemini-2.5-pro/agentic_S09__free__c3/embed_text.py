from embeddings_client import get_embeddings_client


def generate_embedding(text: str) -> list[float]:
    """
    Generates an embedding vector for a single text string.
    """
    client = get_embeddings_client()
    embeddings = client.get_embeddings([text])
    return embeddings[0].values


if __name__ == "__main__":
    text_to_embed = "This is a sample text to generate an embedding for."
    embedding_vector = generate_embedding(text_to_embed)
    print(f"Embedding vector (first 5 dimensions): {embedding_vector[:5]}...")
