import os
from typing import Optional

from dashscope import get_model_list

from model_client import configure_dashscope_client


AVAILABLE_MODELS = {
    "qwen-turbo": {
        "family": "qwen",
        "max_tokens": 8192,
        "context_length": 8192,
        "supports_streaming": True,
        "supports_function_calling": False,
    },
    "qwen-plus": {
        "family": "qwen",
        "max_tokens": 8192,
        "context_length": 32768,
        "supports_streaming": True,
        "supports_function_calling": True,
    },
    "qwen-max": {
        "family": "qwen",
        "max_tokens": 8192,
        "context_length": 8192,
        "supports_streaming": True,
        "supports_function_calling": True,
    },
    "qwen-long": {
        "family": "qwen",
        "max_tokens": 8192,
        "context_length": 1000000,
        "supports_streaming": True,
        "supports_function_calling": False,
    },
}


def select_platform_resource(
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
    required_capabilities: Optional[list[str]] = None,
    max_context_length: Optional[int] = None,
) -> dict:
    configure_dashscope_client(api_key)

    candidates = dict(AVAILABLE_MODELS)

    if model_name:
        if model_name in candidates:
            candidates = {model_name: candidates[model_name]}
        else:
            candidates = {
                k: v for k, v in candidates.items() if model_name.lower() in k.lower()
            }

    if required_capabilities:
        filtered = {}
        for cap in required_capabilities:
            for name, info in candidates.items():
                if cap == "streaming" and info.get("supports_streaming"):
                    filtered[name] = info
                elif cap == "function_calling" and info.get(
                    "supports_function_calling"
                ):
                    filtered[name] = info
        if filtered:
            candidates = filtered

    if max_context_length is not None:
        candidates = {
            name: info
            for name, info in candidates.items()
            if info.get("context_length", 0) <= max_context_length
        }

    if not candidates:
        candidates = {"qwen-turbo": AVAILABLE_MODELS["qwen-turbo"]}

    best_model = next(iter(candidates))
    resource = candidates[best_model]

    return {
        "model_id": best_model,
        "family": resource["family"],
        "max_tokens": resource["max_tokens"],
        "context_length": resource["context_length"],
        "supports_streaming": resource["supports_streaming"],
        "supports_function_calling": resource["supports_function_calling"],
        "platform": "Alibaba Model Studio / DashScope",
        "endpoint": "dashscope.aliyuncs.com",
    }


if __name__ == "__main__":
    resource = select_platform_resource(
        required_capabilities=["streaming"],
        max_context_length=32768,
    )
    print(resource)
