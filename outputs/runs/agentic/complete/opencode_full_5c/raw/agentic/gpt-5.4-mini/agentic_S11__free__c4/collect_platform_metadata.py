from model_client import select_client, load_model_name
from model_models import PlatformRequest, PlatformResponse, normalize_text


def collect_platform_metadata(request: PlatformRequest) -> PlatformResponse:
    client = select_client()
    model = request.model or load_model_name()
    result = client.responses.create(model=model, input=request.prompt)
    usage = getattr(result, "usage", None)
    resource_id = getattr(result, "id", None)
    text = normalize_text(getattr(result, "output_text", None) or result)
    return PlatformResponse(
        text=text, model=model, resource_id=resource_id, usage=usage, raw=result
    )
