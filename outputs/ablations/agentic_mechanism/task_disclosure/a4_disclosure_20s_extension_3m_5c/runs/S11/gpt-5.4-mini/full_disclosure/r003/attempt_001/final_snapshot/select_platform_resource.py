import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class PlatformResource:
    provider: str
    resource_type: str
    resource_id: str
    model: str


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def select_platform_resource(
    model: Optional[str] = None,
    deployment: Optional[str] = None,
    inference_profile: Optional[str] = None,
) -> PlatformResource:
    client = OpenAI(api_key=_env("OPENAI_API_KEY"))
    candidate = model or deployment or inference_profile or _env("OPENAI_MODEL", "gpt-4o-mini")
    resolved = candidate.strip() if candidate else "gpt-4o-mini"
    if deployment:
        resource_type = "deployment"
        resource_id = deployment.strip()
    elif inference_profile:
        resource_type = "inference_profile"
        resource_id = inference_profile.strip()
    else:
        resource_type = "model"
        resource_id = resolved
    _ = client
    return PlatformResource(provider="openai", resource_type=resource_type, resource_id=resource_id, model=resolved)
