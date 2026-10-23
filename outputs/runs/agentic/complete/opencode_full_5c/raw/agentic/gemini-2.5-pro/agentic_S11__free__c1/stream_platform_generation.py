from typing import Iterator
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel, GenerateContentResponse

from model_client import create_client


def stream_model_generation(
    project: str, location: str, model_name: str, prompt: str
) -> Iterator[GenerateContentResponse]:
    create_client(project, location)
    model = GenerativeModel(model_name)
    responses = model.generate_content(prompt, stream=True)
    for response in responses:
        yield response
