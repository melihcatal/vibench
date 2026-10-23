import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_text(text: str) -> list[float]:
    """Generates an embedding vector for a single text string using Google Cloud Vertex AI.

    Args:
        text: The text string to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    vertexai.init(project="your-gcp-project-id", location="us-central1")  # Replace with your GCP project ID and region
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values

