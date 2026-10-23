import vertexai
from vertexai.preview.language_models import TextEmbeddingModel

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generates embeddings for a batch of texts using Google's Vertex AI.

    Args:
        texts: A list of text strings to embed.

    Returns:
        A list of embedding vectors, where each vector corresponds to a text string.
    """
    vertexai.init(project="your-gcp-project-id", location="us-central1") # Replace with your GCP project ID and desired location
    model = TextEmbeddingModel.from_pretrained("text-embedding-gecko@001")
    embeddings = model.get_embeddings(texts)
    return [embedding.values for embedding in embeddings]
