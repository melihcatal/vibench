from __future__ import annotations

from typing import Iterator

from model_client import (
    generation_config_from_request,
    get_vertex_model,
    resolve_vertex_resource,
)
from model_models import (
    PlatformRequest,
    PlatformTextChunk,
    normalize_vertex_text,
    to_vertex_contents,
)


def stream_platform_generation(request: PlatformRequest) -> Iterator[PlatformTextChunk]:
    resource = resolve_vertex_resource()
    model = get_vertex_model(resource)
    stream = model.generate_content(
        contents=to_vertex_contents(request),
        generation_config=generation_config_from_request(request),
        stream=True,
    )
    for chunk in stream:
        yield PlatformTextChunk(
            text=normalize_vertex_text(chunk), candidate_index=0, raw=chunk
        )
