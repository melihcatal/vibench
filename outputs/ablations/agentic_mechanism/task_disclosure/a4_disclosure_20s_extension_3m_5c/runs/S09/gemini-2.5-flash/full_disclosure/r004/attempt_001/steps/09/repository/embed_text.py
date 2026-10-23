import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_text(text: str) -> list[float]:
    """Generates an embedding vector for a single text string using Google's Vertex AI.

    Args:
        text: The input text string to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    vertexai.init(project="your-gcp-project-id", location="us-central1") # Replace with your GCP project ID and desired location
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values

