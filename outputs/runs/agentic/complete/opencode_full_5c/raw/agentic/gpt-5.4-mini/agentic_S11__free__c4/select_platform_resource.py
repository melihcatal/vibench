import os

from model_client import select_client, load_model_name


def resolve_platform_resource(name: str | None = None) -> str:
    model = name or os.getenv("OPENAI_MODEL") or load_model_name()
    client = select_client()
    if hasattr(client, "models"):
        client.models.retrieve(model)
    return model
