from model_client import build_openai_client
from model_models import PlatformRequest, PlatformResponse, normalize_text


def collect_platform_metadata(request: PlatformRequest) -> PlatformResponse:
    client = build_openai_client()
    response = client.responses.create(
        model=request.model, input=normalize_text(request.prompt)
    )
    return PlatformResponse(
        text=getattr(response, "output_text", ""),
        provider_response=response,
        resource_id=getattr(response, "model", request.model),
        metadata={
            "usage": getattr(response, "usage", None),
            "id": getattr(response, "id", None),
        },
    )
