from typing import Optional

import dashscope
from dashscope import get_model_list

from model_client import load_dashscope_api_key
from model_models import ResourceInfo


def select_platform_resource(
    model_id: Optional[str] = None,
    model_family: Optional[str] = None,
    capability: Optional[str] = None,
) -> ResourceInfo:
    load_dashscope_api_key()

    if model_id:
        resolved_model = _resolve_by_model_id(model_id)
    elif model_family:
        resolved_model = _resolve_by_family(model_family, capability)
    else:
        resolved_model = _resolve_default()

    return resolved_model


def _resolve_by_model_id(model_id: str) -> ResourceInfo:
    known_models = {
        "qwen-turbo": {
            "name": "Qwen-Turbo",
            "family": "qwen",
            "capabilities": ["text-generation", "chat"],
            "max_input": 8192,
            "max_output": 1536,
        },
        "qwen-plus": {
            "name": "Qwen-Plus",
            "family": "qwen",
            "capabilities": ["text-generation", "chat", "function-calling"],
            "max_input": 32768,
            "max_output": 8192,
        },
        "qwen-max": {
            "name": "Qwen-Max",
            "family": "qwen",
            "capabilities": [
                "text-generation",
                "chat",
                "function-calling",
                "reasoning",
            ],
            "max_input": 8192,
            "max_output": 8192,
        },
        "qwen-long": {
            "name": "Qwen-Long",
            "family": "qwen",
            "capabilities": ["text-generation", "long-context"],
            "max_input": 1000000,
            "max_output": 8192,
        },
    }

    if model_id in known_models:
        info = known_models[model_id]
        return ResourceInfo(
            model_id=model_id,
            model_name=info["name"],
            model_family=info["family"],
            status="active",
            capabilities=info["capabilities"],
            max_input_tokens=info["max_input"],
            max_output_tokens=info["max_output"],
        )

    response = get_model_list()
    for model_entry in response.data if hasattr(response, "data") else []:
        entry_id = (
            model_entry.get("model", "")
            if isinstance(model_entry, dict)
            else getattr(model_entry, "model", "")
        )
        if entry_id == model_id:
            return ResourceInfo(
                model_id=model_id,
                model_name=model_entry.get("name", model_id)
                if isinstance(model_entry, dict)
                else getattr(model_entry, "name", model_id),
                model_family="qwen",
                status="active",
                capabilities=["text-generation"],
                max_input_tokens=8192,
                max_output_tokens=8192,
                raw_response=response,
            )

    return ResourceInfo(
        model_id=model_id,
        model_name=model_id,
        model_family="qwen",
        status="available",
        capabilities=["text-generation"],
        max_input_tokens=8192,
        max_output_tokens=8192,
    )


def _resolve_by_family(family: str, capability: Optional[str] = None) -> ResourceInfo:
    if family.lower() == "qwen":
        if capability == "long-context":
            return _resolve_by_model_id("qwen-long")
        elif capability == "reasoning":
            return _resolve_by_model_id("qwen-max")
        else:
            return _resolve_by_model_id("qwen-plus")

    return _resolve_default()


def _resolve_default() -> ResourceInfo:
    return _resolve_by_model_id("qwen-plus")
