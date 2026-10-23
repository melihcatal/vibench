from __future__ import annotations

from model_client import PlatformClient
from model_models import PlatformRequest
from select_platform_resource import select_platform_resource


def invoke_platform_model(prompt: str, model_name: str | None = None):
    resource = select_platform_resource(model_name)
    client = PlatformClient()
    request = PlatformRequest(prompt=prompt, model_name=resource.model_id)
    return client.invoke(request)
