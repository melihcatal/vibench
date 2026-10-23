from typing import Optional, List, Dict, Any
from openai import OpenAI
from model_client import create_openai_client, get_openai_api_key
from model_models import PlatformResource


OPENAI_MODEL_REGISTRY: Dict[str, Dict[str, Any]] = {
    "gpt-4o": {
        "resource_id": "openai-gpt-4o-2024-05-13",
        "provider": "openai",
        "status": "active",
        "capabilities": ["chat", "vision", "function_calling", "json_mode"],
        "max_tokens": 16384,
        "context_window": 128000,
        "pricing_tier": "standard",
    },
    "gpt-4o-mini": {
        "resource_id": "openai-gpt-4o-mini-2024-07-18",
        "provider": "openai",
        "status": "active",
        "capabilities": ["chat", "function_calling", "json_mode"],
        "max_tokens": 16384,
        "context_window": 128000,
        "pricing_tier": "economy",
    },
    "gpt-4-turbo": {
        "resource_id": "openai-gpt-4-turbo-2024-04-09",
        "provider": "openai",
        "status": "active",
        "capabilities": ["chat", "vision", "function_calling"],
        "max_tokens": 4096,
        "context_window": 128000,
        "pricing_tier": "premium",
    },
    "o1": {
        "resource_id": "openai-o1-2024-12-17",
        "provider": "openai",
        "status": "active",
        "capabilities": ["chat", "reasoning"],
        "max_tokens": 100000,
        "context_window": 200000,
        "pricing_tier": "premium",
    },
    "o3-mini": {
        "resource_id": "openai-o3-mini-2025-01-31",
        "provider": "openai",
        "status": "active",
        "capabilities": ["chat", "reasoning"],
        "max_tokens": 100000,
        "context_window": 200000,
        "pricing_tier": "standard",
    },
}


def list_available_models(
    client: Optional[OpenAI] = None,
) -> List[PlatformResource]:
    if client is None:
        client = create_openai_client()
    resources = []
    for model_id, info in OPENAI_MODEL_REGISTRY.items():
        resources.append(
            PlatformResource(
                resource_id=info["resource_id"],
                model_name=model_id,
                provider=info["provider"],
                status=info["status"],
                capabilities=info["capabilities"],
                max_tokens=info["max_tokens"],
                context_window=info["context_window"],
                pricing_tier=info["pricing_tier"],
                metadata={
                    "openai_model_id": model_id,
                    "api_endpoint": "https://api.openai.com/v1/chat/completions",
                },
            )
        )
    return resources


def resolve_model_resource(
    model_selector: str,
    client: Optional[OpenAI] = None,
    capability_filter: Optional[List[str]] = None,
    pricing_tier: Optional[str] = None,
) -> PlatformResource:
    if client is None:
        client = create_openai_client()
    if model_selector in OPENAI_MODEL_REGISTRY:
        info = OPENAI_MODEL_REGISTRY[model_selector]
    else:
        for model_id, info in OPENAI_MODEL_REGISTRY.items():
            if model_selector.lower() in model_id.lower():
                break
        else:
            info = OPENAI_MODEL_REGISTRY["gpt-4o"]
    if capability_filter:
        for cap in capability_filter:
            if cap not in info["capabilities"]:
                for mid, minfo in OPENAI_MODEL_REGISTRY.items():
                    if all(c in minfo["capabilities"] for c in capability_filter):
                        info = minfo
                        model_selector = mid
                        break
    if pricing_tier and info.get("pricing_tier") != pricing_tier:
        for mid, minfo in OPENAI_MODEL_REGISTRY.items():
            if minfo.get("pricing_tier") == pricing_tier:
                info = minfo
                model_selector = mid
                break
    return PlatformResource(
        resource_id=info["resource_id"],
        model_name=model_selector,
        provider=info["provider"],
        status=info["status"],
        capabilities=info["capabilities"],
        max_tokens=info["max_tokens"],
        context_window=info["context_window"],
        pricing_tier=info["pricing_tier"],
        metadata={
            "openai_model_id": model_selector,
            "api_endpoint": "https://api.openai.com/v1/chat/completions",
            "resolved_by": "select_platform_resource",
        },
    )


def get_resource_by_capability(
    required_capabilities: List[str],
    client: Optional[OpenAI] = None,
) -> Optional[PlatformResource]:
    if client is None:
        client = create_openai_client()
    for model_id, info in OPENAI_MODEL_REGISTRY.items():
        if all(cap in info["capabilities"] for cap in required_capabilities):
            return PlatformResource(
                resource_id=info["resource_id"],
                model_name=model_id,
                provider=info["provider"],
                status=info["status"],
                capabilities=info["capabilities"],
                max_tokens=info["max_tokens"],
                context_window=info["context_window"],
                pricing_tier=info["pricing_tier"],
                metadata={
                    "openai_model_id": model_id,
                    "api_endpoint": "https://api.openai.com/v1/chat/completions",
                },
            )
    return None
