from model_client import get_client
from model_models import (
    PlatformRequest,
    chunks_from_provider_stream,
    normalize_messages,
)
from select_platform_resource import resolve_resource


def stream_platform_generation(request: PlatformRequest):
    client = get_client()
    resource_id, metadata = resolve_resource(request.model)
    stream = client.chat.completions.create(
        model=request.model,
        messages=normalize_messages(request.prompt),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
    )
    for chunk in chunks_from_provider_stream(stream):
        yield {"resource_id": resource_id, "metadata": metadata, "chunk": chunk}
