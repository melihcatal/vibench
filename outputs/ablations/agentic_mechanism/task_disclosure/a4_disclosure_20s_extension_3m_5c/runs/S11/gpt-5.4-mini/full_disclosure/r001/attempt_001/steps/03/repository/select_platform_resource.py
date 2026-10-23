import os
from dataclasses import dataclass
from typing import Any, Optional

from openai import OpenAI


@dataclass
class PlatformResourceSelection:
    provider: str
    resource_type: str
    resource_id: str
    model: str
    client: Any


def select_platform_resource(
    resource_id: Optional[str] = None,
    model: Optional[str] = None,
    resource_type: Optional[str] = None,
) -> PlatformResourceSelection:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    chosen_resource_id = resource_id or os.environ.get("OPENAI_MODEL") or os.environ.get("OPENAI_DEPLOYMENT") or "gpt-5.4-mini"
    chosen_model = model or chosen_resource_id
    chosen_resource_type = resource_type or ("deployment" if os.environ.get("OPENAI_DEPLOYMENT") else "model")
    return PlatformResourceSelection(
        provider="openai",
        resource_type=chosen_resource_type,
        resource_id=chosen_resource_id,
        model=chosen_model,
        client=client,
    )
