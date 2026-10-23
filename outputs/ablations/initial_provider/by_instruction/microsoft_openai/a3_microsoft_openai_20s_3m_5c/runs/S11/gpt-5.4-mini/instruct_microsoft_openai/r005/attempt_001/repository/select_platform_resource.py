import os
from model_client import get_default_platform_model_name, resolve_platform_resource


def select_platform_resource(preferred: str | None = None) -> str:
    return resolve_platform_resource(preferred or os.environ.get("AZURE_OPENAI_DEPLOYMENT") or get_default_platform_model_name())
