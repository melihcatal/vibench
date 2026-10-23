import os
from typing import Literal, TypedDict

# Supported provider families (used as identifier in code)
Provider = Literal["huggingface", "bedrock", "vertex", "alimt", "alibaba"]


class SelectParams(TypedDict):
    provider: Provider
    deployment_name: str


def select_platform_resource(*, resolve_model: str) -> str:
    """Resolve a provider‑specific model, deployment, or inference resource before invocation.

    In this example we hard‑code the provider to Hugging Face Inference API.
    In a real implementation you would select/look up the appropriate resource here.
    """
    # Example of provider selection logic (choose one based on environment/config)
    provider: Provider = "huggingface"  # <-- concrete provider identifier
    # Map provider to a concrete model identifier
    model_id_map: dict[Provider, str] = {
        "huggingface": resolve_model,  # use the `resolve_model` argument as model name
        "bedrock": "arn:aws:bedrock:model/amazon-Titan-Text-Standard:latest",
        "vertex": "projects/vertex-project/locations/us-central1/publishers/google/models/gemini-pro",
        "alimt": "tianyan-llama3-new-8b chatting",
        "alibaba": "dashscope-llm-demo",
    }
    return model_id_map[provider]
