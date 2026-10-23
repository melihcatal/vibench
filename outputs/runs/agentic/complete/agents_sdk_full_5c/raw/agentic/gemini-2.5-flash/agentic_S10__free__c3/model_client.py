import vertexai
from vertexai.preview.language_models import TextGenerationModel, TextEmbeddingModel

def initialize_vertex_ai(project_id: str, location: str):
    """Initializes Google Cloud Vertex AI with the given project and location."""
    vertexai.init(project=project_id, location=location)

def get_text_generation_model() -> TextGenerationModel:
    """Returns a TextGenerationModel instance for PaLM 2 (text-bison)."""
    return TextGenerationModel.from_pretrained("text-bison@002")

def get_text_embedding_model() -> TextEmbeddingModel:
    """Returns a TextEmbeddingModel instance for text-embedding-004."""
    return TextEmbeddingModel.from_pretrained("text-embedding-004")

