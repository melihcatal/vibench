from __future__ import annotations

from model_client import get_platform_client
from model_models import PlatformRequest, PlatformResponse, normalize_messages
from select_platform_resource import select_platform_resource


def collect_platform_metadata(prompt: str) -> PlatformResponse:
    client = get_platform_client()
    deployment = select_platform_resource()
    req = PlatformRequest(prompt=prompt)
    response = client.chat.completions.create(
        model=deployment, messages=normalize_messages(req)
    )
    text = response.choices[0].message.content or ""
    metadata = {
        "usage": response.usage.model_dump() if response.usage else None,
        "resource_id": deployment,
        "response_id": response.id,
        "model": response.model,
    }
    return PlatformResponse(text=text, provider_metadata=metadata)
