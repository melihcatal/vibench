from dataclasses import dataclass
from typing import Optional

import dashscope
from dashscope import get_model_list

from model_client import (
    load_dashscope_api_key,
    configure_dashscope_client,
    DASHSCOPE_API_HOST,
)

DASHSCOPE_MODEL_CATALOG = {
    "qwen-turbo": {
        "family": "qwen",
        "capabilities": ["chat", "completion"],
        "max_input_tokens": 8192,
        "max_output_tokens": 1536,
        "context_window": 8192,
    },
    "qwen-plus": {
        "family": "qwen",
        "capabilities": ["chat", "completion"],
        "max_input_tokens": 32768,
        "max_output_tokens": 8192,
        "context_window": 32768,
    },
    "qwen-max": {
        "family": "qwen",
        "capabilities": ["chat", "completion"],
        "max_input_tokens": 8192,
        "max_output_tokens": 2048,
        "context_window": 8192,
    },
    "qwen-long": {
        "family": "qwen",
        "capabilities": ["chat", "completion"],
        "max_input_tokens": 1000000,
        "max_output_tokens": 8192,
        "context_window": 1000000,
    },
    "text-embedding-v3": {
        "family": "text-embedding",
        "capabilities": ["embedding"],
        "max_input_tokens": 8192,
        "max_output_tokens": 2048,
        "context_window": 8192,
    },
    "cosyvoice-v1": {
        "family": "cosyvoice",
        "capabilities": ["tts"],
        "max_input_tokens": 0,
        "max_output_tokens": 0,
        "context_window": 0,
    },
}


@dataclass
class ResolvedResource:
    model_id: str
    family: str
    capabilities: list[str]
    max_input_tokens: int
    max_output_tokens: int
    context_window: int
    endpoint: str


def resolve_dashscope_model(
    model_hint: Optional[str] = None,
    capability: str = "chat",
) -> ResolvedResource:
    configure_dashscope_client()

    if model_hint and model_hint in DASHSCOPE_MODEL_CATALOG:
        spec = DASHSCOPE_MODEL_CATALOG[model_hint]
        if capability in spec["capabilities"]:
            return ResolvedResource(
                model_id=model_hint,
                family=spec["family"],
                capabilities=spec["capabilities"],
                max_input_tokens=spec["max_input_tokens"],
                max_output_tokens=spec["max_output_tokens"],
                context_window=spec["context_window"],
                endpoint=DASHSCOPE_API_HOST,
            )

    for model_id, spec in DASHSCOPE_MODEL_CATALOG.items():
        if capability in spec["capabilities"]:
            return ResolvedResource(
                model_id=model_id,
                family=spec["family"],
                capabilities=spec["capabilities"],
                max_input_tokens=spec["max_input_tokens"],
                max_output_tokens=spec["max_output_tokens"],
                context_window=spec["context_window"],
                endpoint=DASHSCOPE_API_HOST,
            )

    raise ValueError(
        f"No DashScope model on {DASHSCOPE_API_HOST} supports capability '{capability}'"
    )


def list_available_dashscope_models() -> list[dict]:
    configure_dashscope_client()
    api_key = load_dashscope_api_key()
    models = get_model_list(api_key=api_key)
    if hasattr(models, "output") and models.output:
        return models.output.get("data", [])
    return []


def select_platform_resource(
    model_hint: Optional[str] = None,
    capability: str = "chat",
) -> ResolvedResource:
    return resolve_dashscope_model(model_hint=model_hint, capability=capability)
