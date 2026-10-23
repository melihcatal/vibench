from google.cloud import aiplatform

def embed_batch(project_id: str, location: str, texts: list[str]) -> list[list[float]]:
    """Generates embeddings for a batch of texts using Vertex AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The region for the Vertex AI endpoint (e.g., "us-central1").
        texts: A list of text strings to embed.

    Returns:
        A list of lists of floats, where each inner list is an embedding vector.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.get_embeddings(texts)
    return [embedding.values for embedding in embeddings]

if __name__ == '__main__':
    # Example usage:
    # project_id = "YOUR_PROJECT_ID"
    # location = "us-central1"
    # texts = ["Hello, world!", "How are you?"]
    # batch_embeddings = embed_batch(project_id, location, texts)
    # for i, embedding in enumerate(batch_embeddings):
    #     print(f"Embedding for text {i}: {embedding[:5]}...")
    pass
