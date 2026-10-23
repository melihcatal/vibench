from model_client import get_generative_model
from model_models import ModelRequest
import vertexai


def stream_platform_generation(request: ModelRequest):
    model = get_generative_model()
    responses = model.generate_content(request.prompt, stream=True, **request.kwargs)
    for response in responses:
        # Preserve the raw response object, which contains provider-specific details
        yield response
