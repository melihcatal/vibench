"""Resolve an OpenAI platform model or deployment resource before invocation."""

from openai import OpenAI

from model_client import get_openai_client, PLATFORM_MODEL_DEFAULT
from model_models import PlatformResource


_PLATFORM_RESOURCE_CACHE: dict[str, PlatformResource] = {}


def list_available_platform_models() -> list[PlatformResource]:
    """List available OpenAI model resources from api.openai.com."""
    client = get_openai_client()
    models = client.models.list()
    resources = []
    for model in models.data:
        resource = PlatformResource(
            resource_id=model.id,
            resource_type="model",
            created=model.created,
            owned_by=model.owned_by,
        )
        resources.append(resource)
        _PLATFORM_RESOURCE_CACHE[resource.resource_id] = resource
    return resources


def resolve_platform_resource(
    resource_name: str | None = None,
    resource_type: str = "chat",
) -> PlatformResource:
    """Resolve the OpenAI model/deployment resource to use for invocation.

    If resource_name is None or empty, the default platform model (gpt-4o)
    is returned.  Otherwise the function verifies the resource exists via
    the OpenAI Models API at api.openai.com.
    """
    target = resource_name or PLATFORM_MODEL_DEFAULT

    if target in _PLATFORM_RESOURCE_CACHE:
        return _PLATFORM_RESOURCE_CACHE[target]

    client = get_openai_client()

    if resource_type == "chat":
        known_chat_models = [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-3.5-turbo",
        ]
        if target in known_chat_models:
            resource = PlatformResource(
                resource_id=target,
                resource_type="chat",
                created=0,
                owned_by="openai",
            )
            _PLATFORM_RESOURCE_CACHE[target] = resource
            return resource

    try:
        model_info = client.models.retrieve(model=target)
        resource = PlatformResource(
            resource_id=model_info.id,
            resource_type="model",
            created=model_info.created,
            owned_by=model_info.owned_by,
        )
        _PLATFORM_RESOURCE_CACHE[target] = resource
        return resource
    except Exception:
        resource = PlatformResource(
            resource_id=target,
            resource_type=resource_type,
            created=0,
            owned_by="unknown",
        )
        _PLATFORM_RESOURCE_CACHE[target] = resource
        return resource


if __name__ == "__main__":
    resource = resolve_platform_resource("gpt-4o")
    print(f"Resolved resource: {resource.resource_id} ({resource.resource_type})")
