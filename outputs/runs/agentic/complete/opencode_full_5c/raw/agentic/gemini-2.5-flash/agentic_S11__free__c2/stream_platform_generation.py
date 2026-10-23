import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part


def stream_generation(project_id: str, location: str, model_name: str, prompt: str):
    """Streams output from a Google Cloud Vertex AI generative model."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    responses = model.generate_content(prompt, stream=True)
    return [response for response in responses]
