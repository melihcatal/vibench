import vertexai
from vertexai.preview.language_models import TextGenerationModel

def invoke_platform_model(project_id: str, location: str, model_id: str, prompt: str) -> str:
    """Invokes a Google Cloud Vertex AI model."""
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained(model_id)
    response = model.predict(prompt=prompt)
    return response.text
