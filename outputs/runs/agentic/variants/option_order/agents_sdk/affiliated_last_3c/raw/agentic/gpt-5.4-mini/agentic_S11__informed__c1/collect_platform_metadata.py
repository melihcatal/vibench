from __future__ import annotations

from model_client import PlatformClient
from model_models import PlatformRequest, NormalizedOutput
from select_platform_resource import select_platform_resource


def collect_platform_metadata(prompt: str, model_name: str | None = None) -> NormalizedOutput:
    resource = select_platform_resource(model_name)
    client = PlatformClient()
    response = client.invoke(PlatformRequest(prompt=prompt, model_name=resource.model_id))
    return NormalizedOutput(text=response.text, metadata=client.metadata(response))
