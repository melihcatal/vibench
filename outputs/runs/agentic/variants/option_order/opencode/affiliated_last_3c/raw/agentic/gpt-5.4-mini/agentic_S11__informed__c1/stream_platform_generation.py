from model_client import get_client, load_config
from model_models import PlatformRequest, stream_text
from select_platform_resource import select_platform_resource


def stream_platform_generation(request: PlatformRequest, resource: str | None = None):
    cfg = load_config()
    client = get_client()
    deployment = select_platform_resource(resource)
    stream = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": request.prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
    )
    collected = []
    for chunk in stream:
        collected.append(chunk)
        yield {"chunk": chunk, "model": cfg.model, "resource_id": deployment}
    yield {
        "chunk": None,
        "text": stream_text(collected),
        "model": cfg.model,
        "resource_id": deployment,
    }
