from vertexai.preview.language_models import TextEmbeddingModel
from typing import List

def get_text_embeddings(project_id: str, location: str, texts: List[str]) -> List[List[float]]:
    """Generates embeddings for a list of texts using Google Cloud Vertex AI TextEmbeddingModel."""
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings(texts)
    return [embedding.values for embedding in embeddings]

