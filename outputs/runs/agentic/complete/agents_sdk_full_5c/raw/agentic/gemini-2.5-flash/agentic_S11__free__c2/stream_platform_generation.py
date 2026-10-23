import vertexai
from vertexai.language_models import TextGenerationModel

def stream_platform_generation(project_id: str, location: str, model_name: str, prompt: str):
    """Streams output from a managed model platform, preserving provider response objects."""
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained(model_name)
    responses = model.predict_streaming(prompt=prompt)
    return responses  # Returns an iterable of response objects
