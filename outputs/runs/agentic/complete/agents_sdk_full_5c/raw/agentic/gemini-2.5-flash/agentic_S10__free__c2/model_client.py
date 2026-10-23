import vertexai
from vertexai.generative_models import GenerativeModel

# Vertex AI provider-identifying signal: vertexai import, GenerativeModel class

def init_vertex_ai(project_id: str, location: str = "us-central1"):
    """Initializes Vertex AI SDK."""
    vertexai.init(project=project_id, location=location)

def get_generative_model(model_name: str = "gemini-pro"):
    """Returns a GenerativeModel instance for text generation."""
    return GenerativeModel(model_name)

def get_embedding_model(model_name: str = "text-embedding-004"):
    """Returns a TextEmbeddingModel instance for text embeddings."""
    from vertexai.language_models import TextEmbeddingModel
    return TextEmbeddingModel.from_pretrained(model_name)
