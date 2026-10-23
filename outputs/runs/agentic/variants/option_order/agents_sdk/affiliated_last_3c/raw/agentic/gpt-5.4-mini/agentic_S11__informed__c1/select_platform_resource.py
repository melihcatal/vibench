from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from model_client import PlatformClient


@dataclass
class PlatformResource:
    model_id: str
    deployment_name: str


AZURE_DEPLOYMENT_ALIASES = {
    "default": "gpt-4o-mini",
    "compact": "gpt-4o-mini",
    "reasoning": "gpt-4.1-mini",
}


def select_platform_resource(preferred: Optional[str] = None) -> PlatformResource:
    client = PlatformClient()
    model_id = client.select_model(AZURE_DEPLOYMENT_ALIASES.get(preferred or "default", preferred))
    deployment_name = model_id
    return PlatformResource(model_id=model_id, deployment_name=deployment_name)
