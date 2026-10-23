import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class PlatformResource:
    provider: str
    resource: str
    kind: str


def select_platform_resource(explicit_resource: Optional[str] = None) -> PlatformResource:
    resource = explicit_resource or os.getenv("OPENAI_MODEL") or os.getenv("OPENAI_DEPLOYMENT") or "gpt-5.4-mini"
    client = OpenAI()
    if resource.startswith("ft:") or resource.startswith("gpt-") or resource.startswith("openai/"):
        resolved = resource.replace("openai/", "")
        return PlatformResource(provider="openai", resource=resolved, kind="model")
    models = client.models.list()
    for item in models.data:
        if getattr(item, "id", None) == resource:
            return PlatformResource(provider="openai", resource=resource, kind="model")
    return PlatformResource(provider="openai", resource=resource, kind="deployment")
