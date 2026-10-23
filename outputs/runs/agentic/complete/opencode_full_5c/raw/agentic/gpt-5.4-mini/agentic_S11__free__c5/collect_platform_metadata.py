from model_client import create_platform_client
from model_models import PlatformResponse
from select_platform_resource import select_platform_resource


def collect_platform_metadata(prompt: str) -> PlatformResponse:
    client = create_platform_client()
    model = select_platform_resource()
    response = client.responses.create(model=model, input=prompt)
    return PlatformResponse(
        text=getattr(response, "output_text", ""),
        model=getattr(response, "model", model),
        usage=getattr(response, "usage", None),
        resource_id=getattr(response, "id", None),
    )
