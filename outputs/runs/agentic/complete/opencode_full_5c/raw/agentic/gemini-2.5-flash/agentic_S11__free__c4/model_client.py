import vertexai
import os


def initialize_vertex_client():
    """Initializes the Vertex AI client."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    vertexai.init(project=project_id, location=location)


def get_text_generation_model(model_name: str = "gemini-pro"):
    """Returns a TextGenerationModel instance."""
    from vertexai.preview.language_models import TextGenerationModel

    return TextGenerationModel.from_pretrained(model_name)


def get_generative_model(model_name: str = "gemini-pro"):
    """Returns a GenerativeModel instance."""
    from vertexai.generative_models import GenerativeModel

    return GenerativeModel(model_name)


def get_text_embedding_model(model_name: str = "text-embedding-004"):
    """Returns a TextEmbeddingModel instance."""
    from vertexai.language_models import TextEmbeddingModel

    return TextEmbeddingModel.from_pretrained(model_name)
