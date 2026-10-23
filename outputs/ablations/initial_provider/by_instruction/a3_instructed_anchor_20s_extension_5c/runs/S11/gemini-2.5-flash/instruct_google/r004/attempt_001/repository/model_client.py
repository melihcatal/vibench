from google.cloud import aiplatform

def get_vertex_ai_client(project_id: str, location: str):
    """Provides a configured Google Vertex AI client."""
    aiplatform.init(project=project_id, location=location)
    return aiplatform

def get_text_generation_model(model_id: str):
    """Returns a TextGenerationModel instance from Vertex AI."""
    return aiplatform.TextGenerationModel.from_pretrained(model_id)
