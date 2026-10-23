from google.cloud import aiplatform

def embed_text(text: str) -> list[float]:
    """
    Embeds the given text using a Google Cloud Generative AI embedding model.

    Args:
        text: The text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    # Initialize the AI Platform client
    # Replace 'your-project-id' and 'your-location' with your actual GCP project ID and region
    aiplatform.init(project='your-project-id', location='us-central1')

    # Use the TextEmbeddingModel to get embeddings
    # The model ID 'text-embedding-004' is an example. Choose the appropriate model for your needs.
    model = aiplatform.language_models.TextEmbeddingModel.from_pretrained("text-embedding-gecko@003")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values

