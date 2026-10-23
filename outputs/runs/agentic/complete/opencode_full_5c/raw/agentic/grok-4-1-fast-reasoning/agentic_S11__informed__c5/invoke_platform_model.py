from model_client import get_platform_client
from model_models import GenerationRequest, GenerationResponse
from select_platform_resource import select_platform_resource


def invoke_platform_model(request: GenerationRequest) -> GenerationResponse:
    client = get_platform_client()
    deployment_id = select_platform_resource(request["model"])
    kwargs = {
        "model": deployment_id,
        "messages": request["messages"],
    }
    if "max_tokens" in request:
        kwargs["max_tokens"] = request["max_tokens"]
    if "temperature" in request:
        kwargs["temperature"] = request["temperature"]
    response = client.chat.completions.create(**kwargs)
    usage = response.usage.model_dump() if hasattr(response.usage, "model_dump") else {}
    return {"content": response.choices[0].message.content, "usage": usage}
