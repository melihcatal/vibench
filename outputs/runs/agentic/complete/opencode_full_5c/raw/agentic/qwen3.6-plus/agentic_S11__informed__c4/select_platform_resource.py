from typing import Optional

import dashscope
from dashscope import ModelList

from model_client import load_dashscope_config


DASHSCOPE_MODEL_REGISTRY = {
    "qwen-turbo": {
        "model_id": "qwen-turbo",
        "provider": "dashscope",
        "service": "Alibaba Model Studio / DashScope",
        "capabilities": ["text-generation", "chat"],
        "max_tokens": 8192,
        "context_length": 8192,
    },
    "qwen-plus": {
        "model_id": "qwen-plus",
        "provider": "dashscope",
        "service": "Alibaba Model Studio / DashScope",
        "capabilities": ["text-generation", "chat"],
        "max_tokens": 32768,
        "context_length": 32768,
    },
    "qwen-max": {
        "model_id": "qwen-max",
        "provider": "dashscope",
        "service": "Alibaba Model Studio / DashScope",
        "capabilities": ["text-generation", "chat"],
        "max_tokens": 8192,
        "context_length": 8192,
    },
    "qwen-long": {
        "model_id": "qwen-long",
        "provider": "dashscope",
        "service": "Alibaba Model Studio / DashScope",
        "capabilities": ["text-generation", "chat", "long-context"],
        "max_tokens": 32768,
        "context_length": 1000000,
    },
}


def resolve_model_resource(
    model_name: Optional[str] = None,
    capability: Optional[str] = None,
    min_context_length: int = 0,
) -> dict:
    config = load_dashscope_config()
    target_model = model_name or "qwen-turbo"
    if target_model not in DASHSCOPE_MODEL_REGISTRY:
        raise ValueError(
            f"Model '{target_model}' not found in DashScope registry. "
            f"Available models: {list(DASHSCOPE_MODEL_REGISTRY.keys())}"
        )
    resource = DASHSCOPE_MODEL_REGISTRY[target_model].copy()
    if capability and capability not in resource["capabilities"]:
        raise ValueError(
            f"Model '{target_model}' does not support capability '{capability}'"
        )
    if min_context_length > 0 and resource["context_length"] < min_context_length:
        raise ValueError(
            f"Model '{target_model}' context length {resource['context_length']} "
            f"is below required {min_context_length}"
        )
    resource["resource_id"] = f"dashscope://{resource['model_id']}"
    resource["api_endpoint"] = (
        "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    )
    return resource


def list_available_resources() -> list:
    load_dashscope_config()
    resources = []
    for model_id, info in DASHSCOPE_MODEL_REGISTRY.items():
        resource = info.copy()
        resource["resource_id"] = f"dashscope://{model_id}"
        resource["api_endpoint"] = (
            "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        )
        resources.append(resource)
    return resources


def get_resource_by_capability(capability: str, min_context_length: int = 0) -> dict:
    load_dashscope_config()
    best_match = None
    best_context = 0
    for model_id, info in DASHSCOPE_MODEL_REGISTRY.items():
        if capability in info["capabilities"]:
            if (
                info["context_length"] >= min_context_length
                and info["context_length"] > best_context
            ):
                best_match = info
                best_context = info["context_length"]
    if best_match is None:
        raise ValueError(
            f"No DashScope model found with capability '{capability}' "
            f"and minimum context length {min_context_length}"
        )
    resource = best_match.copy()
    resource["resource_id"] = f"dashscope://{resource['model_id']}"
    resource["api_endpoint"] = (
        "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    )
    return resource
