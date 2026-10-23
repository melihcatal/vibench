import vertexai
from vertexai.preview.language_models import TextEmbeddingModel

def embed_metadata_and_text(text: str) -> list[float]:
    """Embeds object metadata and extracted text for search using Google's TextEmbeddingModel.

    Args:
        text: The text to embed, which can include object metadata and extracted content.

    Returns:
        A list of floats representing the embedding vector.
    """
    vertexai.init(project="your-gcp-project-id", location="us-central1") # Replace with your GCP project ID
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values

