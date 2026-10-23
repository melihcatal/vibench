import vertexai
from vertexai.language_models import TextEmbeddingModel


def initialize_vertex_ai(project: str, location: str):
    """Initializes Vertex AI for a given project and location."""
    vertexai.init(project=project, location=location)


def get_embedding_model() -> TextEmbeddingModel:
    """Returns the Vertex AI TextEmbeddingModel."""
    return TextEmbeddingModel.from_pretrained("text-embedding-004")
