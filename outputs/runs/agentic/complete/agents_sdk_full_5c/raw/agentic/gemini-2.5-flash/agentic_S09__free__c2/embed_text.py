from google.cloud import aiplatform

def embed_text(project_id: str, location: str, text: str) -> list[float]:
    """Generates an embedding vector for a single text string using Vertex AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The region for the Vertex AI endpoint (e.g., "us-central1").
        text: The text string to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values

if __name__ == '__main__':
    # This is a placeholder for actual usage.
    # Replace with your project_id and desired location.
    # print(embed_text(project_id="your-project-id", location="us-central1", text="Hello world"))
    pass
