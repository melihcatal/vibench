from __future__ import annotations

from model_client import get_platform_client
from model_models import PlatformRequest, PlatformResponse, normalize_messages
from select_platform_resource import select_platform_resource


def invoke_platform_model(prompt: str, system: str = "") -> PlatformResponse:
    client = get_platform_client()
    deployment = select_platform_resource()
    req = PlatformRequest(prompt=prompt, system=system)
    response = client.chat.completions.create(
        model=deployment,
        messages=normalize_messages(req),
        temperature=req.temperature,
        max_tokens=req.max_tokens,
    )
    text = response.choices[0].message.content or ""
    return PlatformResponse(
        text=text,
        provider_metadata={
            "id": response.id,
            "model": response.model,
            "usage": response.usage.model_dump() if response.usage else None,
        },
    )
