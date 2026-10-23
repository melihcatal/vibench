from model_client import get_platform_client
from model_models import GenerationRequest, PlatformStreamResponse
from select_platform_resource import select_platform_resource


def stream_platform_generation(request: GenerationRequest) -> PlatformStreamResponse:
    client = get_platform_client()
    deployment_id = select_platform_resource(request["model"])
    kwargs = {
        "model": deployment_id,
        "messages": request["messages"],
        "stream": True,
    }
    if "max_tokens" in request:
        kwargs["max_tokens"] = request["max_tokens"]
    if "temperature" in request:
        kwargs["temperature"] = request["temperature"]
    stream = client.chat.completions.create(**kwargs)
    return stream
