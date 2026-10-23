import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass
class PlatformResource:
    provider: str
    resource_type: str
    resource_id: str
    handle: str
    metadata: Dict[str, Any]


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def _select_chat_model(preferred: Optional[str] = None) -> PlatformResource:
    model = preferred or os.environ.get("OPENAI_MODEL") or "gpt-4.1-mini"
    return PlatformResource(
        provider="openai",
        resource_type="model",
        resource_id=model,
        handle=model,
        metadata={"api_base": "https://api.openai.com/v1", "client": "openai-python"},
    )


def select_platform_resource(
    resource_kind: str = "model",
    preferred_resource: Optional[str] = None,
) -> PlatformResource:
    if resource_kind not in {"model", "deployment", "inference_profile"}:
        raise ValueError("resource_kind must be one of: model, deployment, inference_profile")

    if resource_kind == "model":
        return _select_chat_model(preferred_resource)

    client = _client()
    if resource_kind == "deployment":
        deployment_id = preferred_resource or os.environ.get("OPENAI_DEPLOYMENT_ID")
        if not deployment_id:
            raise ValueError("Missing deployment identifier for OpenAI platform resource selection")
        return PlatformResource(
            provider="openai",
            resource_type="deployment",
            resource_id=deployment_id,
            handle=deployment_id,
            metadata={"client": client.__class__.__name__},
        )

    profile_id = preferred_resource or os.environ.get("OPENAI_INFERENCE_PROFILE_ID")
    if not profile_id:
        raise ValueError("Missing inference profile identifier for OpenAI platform resource selection")
    return PlatformResource(
        provider="openai",
        resource_type="inference_profile",
        resource_id=profile_id,
        handle=profile_id,
        metadata={"client": client.__class__.__name__},
    )
