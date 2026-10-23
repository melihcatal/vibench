from __future__ import annotations

from model_client import (
    generation_config_from_request,
    get_vertex_model,
    resolve_vertex_resource,
)
from model_models import (
    PlatformRequest,
    PlatformResponse,
    normalize_usage_metadata,
    normalize_vertex_text,
    to_vertex_contents,
)


def invoke_platform_model(request: PlatformRequest) -> PlatformResponse:
    resource = resolve_vertex_resource()
    model = get_vertex_model(resource)
    response = model.generate_content(
        contents=to_vertex_contents(request),
        generation_config=generation_config_from_request(request),
    )
    return PlatformResponse(
        text=normalize_vertex_text(response),
        model=resource.model,
        resource_name=resource.full_model_name,
        usage=normalize_usage_metadata(response),
        raw=response,
    )
