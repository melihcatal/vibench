from model_client import initialize_vertexai, get_generative_model
from model_models import ModelRequest, ModelResponse
import os
from typing import Generator


def stream_platform_generation(
    request: ModelRequest, project_id: str, location: str, model_id: str
) -> Generator[ModelResponse, None, None]:
    initialize_vertexai(project_id, location)
    model = get_generative_model(model_id)
    responses = model.generate_content(request.prompt, stream=True)
    for response in responses:
        yield ModelResponse(
            text=response.text, metadata={"raw_response_object": response}
        )
