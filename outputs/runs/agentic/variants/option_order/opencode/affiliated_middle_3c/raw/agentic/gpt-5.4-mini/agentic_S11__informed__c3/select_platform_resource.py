import os
from model_client import load_platform_config


def select_platform_resource(preferred_model: str | None = None) -> str:
    config = load_platform_config()
    if preferred_model:
        return preferred_model
    return config.get("AZURE_OPENAI_MODEL", "gpt-4.1-mini")
