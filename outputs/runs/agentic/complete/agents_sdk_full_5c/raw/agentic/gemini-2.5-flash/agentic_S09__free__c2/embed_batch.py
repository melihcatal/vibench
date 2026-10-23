from google.cloud import aiplatform

def embed_batch(project_id: str, location: str, texts: list[str]) -> list[list[float]]:
    """Generates embedding vectors for a batch of text strings using Vertex AI.

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
    # This is a placeholder for actual usage.
    # Replace with your project_id and desired location.
    # print(embed_batch(project_id="your-project-id", location="us-central1", texts=["Hello world", "How are you?"]))
    pass
