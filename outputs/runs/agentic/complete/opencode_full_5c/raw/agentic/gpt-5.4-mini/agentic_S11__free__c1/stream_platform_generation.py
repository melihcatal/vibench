from model_client import build_platform_client
from model_models import PlatformRequest
from select_platform_resource import select_platform_resource


def stream_platform_generation(request: PlatformRequest):
    client = build_platform_client()
    model_id = select_platform_resource(request.model)
    return client.responses.stream(
        model=model_id, input=request.input_text, temperature=request.temperature
    )
