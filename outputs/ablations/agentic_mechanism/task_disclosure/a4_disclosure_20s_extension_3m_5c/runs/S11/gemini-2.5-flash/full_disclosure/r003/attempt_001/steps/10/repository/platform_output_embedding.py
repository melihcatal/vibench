import vertexai
from vertexai.preview.language_models import TextEmbeddingModel

def embed_platform_output(text: str) -> list[float]:
    """
    Embeds platform outputs for evaluation or retrieval using Google's Vertex AI.

    Args:
        text: The text content to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    vertexai.init(project="your-gcp-project-id", location="us-central1") # Replace with your GCP project ID and region
    model = TextEmbeddingModel.from_pretrained("text-embedding-gecko@003")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values
