from model_client import get_vertex_client
from vertexai.generative_models import GenerativeModel
from model_models import PlatformModelRequest, PlatformModelResponse


def invoke_model(request: PlatformModelRequest) -> PlatformModelResponse:
    """
    Invokes a specified model on Vertex AI.
    """
    get_vertex_client()

    model = GenerativeModel(request.model_id)

    response = model.generate_content(request.prompt)

    return PlatformModelResponse(text=response.text, raw_response=response)
