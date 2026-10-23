from google.cloud import aiplatform
from typing import List

def embed_asset_metadata_and_text(
    texts: List[str],
    project_id: str,
    location: str = "us-central1"
) -> List[List[float]]:
    """Embeds object metadata and extracted text for search using Google Cloud Vertex AI (text-embedding-004 model)."""
    aiplatform.init(project=project_id, location=location)

    # Using the text-embedding-004 model
    # More information: https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/text-embeddings
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings(texts)

    return [embedding.values for embedding in embeddings]
