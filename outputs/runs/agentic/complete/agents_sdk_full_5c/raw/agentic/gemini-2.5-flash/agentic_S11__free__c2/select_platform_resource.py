import vertexai
from vertexai.language_models import TextGenerationModel

def select_platform_resource(project_id: str, location: str, model_id: str):
    """Resolves a provider-specific model resource."""
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained(model_id)
    # In Vertex AI, 'from_pretrained' implicitly selects and loads the model resource.
    # We can return the model object itself or its ID as confirmation.
    return model.model_id
