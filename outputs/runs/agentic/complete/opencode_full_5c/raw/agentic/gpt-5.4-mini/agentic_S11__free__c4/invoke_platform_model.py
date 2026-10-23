from model_client import select_client, load_model_name
from model_models import PlatformRequest, PlatformResponse, normalize_text


def invoke_platform_model(request: PlatformRequest) -> PlatformResponse:
    client = select_client()
    model = request.model or load_model_name()
    result = client.responses.create(
        model=model,
        input=request.prompt,
    )
    text = normalize_text(
        getattr(result, "output_text", None)
        or getattr(result, "output", None)
        or result
    )
    return PlatformResponse(text=text, model=model, raw=result)
