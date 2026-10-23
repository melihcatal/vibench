import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part


def stream_platform_generation(
    project_id: str, location: str, model_name: str, prompt: str
):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    responses = model.generate_content(prompt, stream=True)
    for response in responses:
        yield response.text
