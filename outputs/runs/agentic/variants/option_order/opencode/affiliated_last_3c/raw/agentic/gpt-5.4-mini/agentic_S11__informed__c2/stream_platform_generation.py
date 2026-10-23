from model_client import get_client, resolve_model_id
from model_models import PlatformRequest


def stream_platform_generation(request: PlatformRequest):
    client = get_client()
    model_id = request.model_id or resolve_model_id()
    return client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": request.prompt}],
        stream=True,
    )
