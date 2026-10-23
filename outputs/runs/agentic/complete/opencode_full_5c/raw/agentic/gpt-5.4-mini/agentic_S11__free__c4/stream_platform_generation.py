from model_client import select_client, load_model_name
from model_models import PlatformRequest, normalize_text


def stream_platform_generation(request: PlatformRequest):
    client = select_client()
    model = request.model or load_model_name()
    stream = client.responses.create(model=model, input=request.prompt, stream=True)
    for event in stream:
        yield (
            event,
            normalize_text(
                getattr(event, "delta", None) or getattr(event, "text", None) or ""
            ),
        )
