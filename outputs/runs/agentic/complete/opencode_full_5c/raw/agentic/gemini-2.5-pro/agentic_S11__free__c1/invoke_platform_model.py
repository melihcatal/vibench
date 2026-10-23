from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel

from model_client import create_client
from model_models import ModelResponse


def invoke_model(
    project: str, location: str, model_name: str, prompt: str
) -> ModelResponse:
    create_client(project, location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return ModelResponse(text=response.text, raw_response=response)
