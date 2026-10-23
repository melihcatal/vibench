import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part


def invoke_model(project_id: str, location: str, model_name: str, prompt: str):
    """Invokes a Google Cloud Vertex AI generative model."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text
