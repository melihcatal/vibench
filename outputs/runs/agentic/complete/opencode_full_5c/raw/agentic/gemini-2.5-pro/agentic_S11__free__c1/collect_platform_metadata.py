from typing import Dict, Any
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel

from model_client import create_client
from model_models import ModelResponseWithMetadata


def get_model_response_with_metadata(
    project: str, location: str, model_name: str, prompt: str
) -> ModelResponseWithMetadata:
    create_client(project, location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)

    metadata = {
        "usage": {
            "prompt_token_count": response.usage_metadata.prompt_token_count,
            "candidates_token_count": response.usage_metadata.candidates_token_count,
            "total_token_count": response.usage_metadata.total_token_count,
        }
    }

    return ModelResponseWithMetadata(
        text=response.text, metadata=metadata, raw_response=response
    )
