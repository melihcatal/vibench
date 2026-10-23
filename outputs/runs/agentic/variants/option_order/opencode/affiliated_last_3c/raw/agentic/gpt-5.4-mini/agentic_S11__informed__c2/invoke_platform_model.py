from model_client import get_client, resolve_model_id
from model_models import PlatformRequest, PlatformResponse, response_text_from_choice


def invoke_platform_model(request: PlatformRequest) -> PlatformResponse:
    client = get_client()
    model_id = request.model_id or resolve_model_id()
    response = client.chat.completions.create(
        model=model_id, messages=[{"role": "user", "content": request.prompt}]
    )
    return PlatformResponse(
        text=response_text_from_choice(response),
        usage=getattr(response, "usage", None),
        resource_id=model_id,
        model_id=model_id,
        raw=response,
    )
