import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI

from model_client import get_openai_client, get_model_name


@dataclass
class PlatformResource:
    model: str
    resource_id: str
    client: OpenAI


def select_platform_resource(resource_id: Optional[str] = None) -> PlatformResource:
    client = get_openai_client()
    model = get_model_name(default="gpt-4.1-mini")
    resolved_resource_id = resource_id or os.environ.get("OPENAI_MODEL_RESOURCE_ID") or model
    return PlatformResource(model=model, resource_id=resolved_resource_id, client=client)
