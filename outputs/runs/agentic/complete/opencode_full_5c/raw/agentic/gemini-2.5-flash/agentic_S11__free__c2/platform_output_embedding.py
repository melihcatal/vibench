import vertexai
from vertexai.preview.language_models import TextEmbeddingModel


def embed_output(project_id: str, location: str, texts: list[str]):
    """Embeds platform outputs for evaluation or retrieval using Google Cloud Vertex AI Embedding API."""
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings(texts)
    return [embedding.values for embedding in embeddings]
