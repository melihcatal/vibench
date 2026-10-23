import vertexai
from vertexai.language_models import TextGenerationModel, TextEmbeddingModel

class VertexAIClient:
    """Provides a configured client for Vertex AI models."""
    def __init__(self, project_id: str, location: str):
        self.project_id = project_id
        self.location = location
        vertexai.init(project=self.project_id, location=self.location)

    def get_text_generation_model(self, model_name: str) -> TextGenerationModel:
        """Returns a TextGenerationModel instance."""
        return TextGenerationModel.from_pretrained(model_name)

    def get_text_embedding_model(self, model_name: str) -> TextEmbeddingModel:
        """Returns a TextEmbeddingModel instance."""
        return TextEmbeddingModel.from_pretrained(model_name)


# Example of loading configuration (can be extended with env vars or config files)
def load_vertex_ai_config():
    return {"project_id": "your-gcp-project-id", "location": "us-central1"}
