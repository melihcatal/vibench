from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI

from model_client import PlatformClientConfig, create_openai_client


@dataclass
class ResolvedResource:
    model_id: str
    provider: str
    capability: str
    context_window: int
    max_output_tokens: int
    supports_vision: bool
    supports_function_calling: bool
    raw_model_object: Optional[dict] = None


OPENAI_MODEL_REGISTRY: dict[str, dict] = {
    "gpt-4o": {
        "capability": "chat",
        "context_window": 128000,
        "max_output_tokens": 16384,
        "supports_vision": True,
        "supports_function_calling": True,
    },
    "gpt-4o-mini": {
        "capability": "chat",
        "context_window": 128000,
        "max_output_tokens": 16384,
        "supports_vision": True,
        "supports_function_calling": True,
    },
    "gpt-4-turbo": {
        "capability": "chat",
        "context_window": 128000,
        "max_output_tokens": 4096,
        "supports_vision": True,
        "supports_function_calling": True,
    },
    "gpt-3.5-turbo": {
        "capability": "chat",
        "context_window": 16385,
        "max_output_tokens": 4096,
        "supports_vision": False,
        "supports_function_calling": True,
    },
    "text-embedding-3-large": {
        "capability": "embedding",
        "context_window": 8191,
        "max_output_tokens": 0,
        "supports_vision": False,
        "supports_function_calling": False,
    },
    "text-embedding-3-small": {
        "capability": "embedding",
        "context_window": 8191,
        "max_output_tokens": 0,
        "supports_vision": False,
        "supports_function_calling": False,
    },
    "tts-1": {
        "capability": "audio",
        "context_window": 0,
        "max_output_tokens": 0,
        "supports_vision": False,
        "supports_function_calling": False,
    },
    "whisper-1": {
        "capability": "transcription",
        "context_window": 0,
        "max_output_tokens": 0,
        "supports_vision": False,
        "supports_function_calling": False,
    },
}


def select_platform_resource(
    model_name: Optional[str] = None,
    capability: str = "chat",
    require_vision: bool = False,
    require_function_calling: bool = False,
    client: Optional[OpenAI] = None,
    config: Optional[PlatformClientConfig] = None,
) -> ResolvedResource:
    target = model_name or os.environ.get("OPENAI_MODEL", "gpt-4o")

    if target in OPENAI_MODEL_REGISTRY:
        info = OPENAI_MODEL_REGISTRY[target]
        return ResolvedResource(
            model_id=target,
            provider="openai",
            capability=info["capability"],
            context_window=info["context_window"],
            max_output_tokens=info["max_output_tokens"],
            supports_vision=info["supports_vision"],
            supports_function_calling=info["supports_function_calling"],
            raw_model_object={"id": target, "object": "model", "owned_by": "openai"},
        )

    openai_client = client or create_openai_client(config)

    try:
        models = openai_client.models.list()
        for m in models.data:
            if m.id == target:
                return ResolvedResource(
                    model_id=target,
                    provider="openai",
                    capability=capability,
                    context_window=0,
                    max_output_tokens=0,
                    supports_vision=False,
                    supports_function_calling=False,
                    raw_model_object=m.model_dump(),
                )
    except Exception:
        pass

    return ResolvedResource(
        model_id=target,
        provider="openai",
        capability=capability,
        context_window=128000,
        max_output_tokens=4096,
        supports_vision=require_vision,
        supports_function_calling=require_function_calling,
    )


def list_available_openai_models(
    client: Optional[OpenAI] = None,
    config: Optional[PlatformClientConfig] = None,
) -> list[ResolvedResource]:
    openai_client = client or create_openai_client(config)
    models = openai_client.models.list()
    resources = []
    for m in models.data:
        info = OPENAI_MODEL_REGISTRY.get(m.id, {})
        resources.append(
            ResolvedResource(
                model_id=m.id,
                provider="openai",
                capability=info.get("capability", "unknown"),
                context_window=info.get("context_window", 0),
                max_output_tokens=info.get("max_output_tokens", 0),
                supports_vision=info.get("supports_vision", False),
                supports_function_calling=info.get("supports_function_calling", False),
                raw_model_object=m.model_dump(),
            )
        )
    return resources


if __name__ == "__main__":
    resource = select_platform_resource(model_name="gpt-4o")
    print(f"Selected: {resource.model_id} (provider={resource.provider})")
