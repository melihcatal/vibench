import embeddings_client

# Direct Embeddings API integration (example provider: OpenAI)


def embed_text(text: str) -> list:
    """Generate a single embedding vector for the provided text.
    Returns a list of floats representing the embedding.
    """
    client = embeddings_client.EmbeddingsClient()
    response = client.create_embedding(
        model="text-embedding-ada-002",  # OpenAI model identifier
        input=text,
    )
    # Assume response contains a list of floats under 'embedding' field
    return response["embedding"]
