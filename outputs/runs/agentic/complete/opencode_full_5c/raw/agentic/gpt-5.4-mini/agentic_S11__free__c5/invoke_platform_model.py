from model_client import create_platform_client
from model_models import PlatformRequest, PlatformResponse
from select_platform_resource import select_platform_resource


def invoke_platform_model(prompt: str) -> PlatformResponse:
    client = create_platform_client()
    model = select_platform_resource()
    req = PlatformRequest(prompt=prompt)
    response = client.responses.create(
        model=model, input=req.prompt, temperature=req.temperature
    )
    text = getattr(response, "output_text", "")
    return PlatformResponse(
        text=text,
        model=getattr(response, "model", model),
        usage=getattr(response, "usage", None),
        resource_id=getattr(response, "id", None),
    )
