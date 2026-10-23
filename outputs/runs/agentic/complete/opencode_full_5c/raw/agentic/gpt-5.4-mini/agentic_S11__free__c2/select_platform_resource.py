from openai import OpenAI

from model_client import build_platform_client, load_platform_config


def select_platform_resource(preferred_model: str | None = None) -> str:
    cfg = load_platform_config()
    client: OpenAI = build_platform_client(cfg)
    model = preferred_model or cfg.model
    models = client.models.list()
    for item in models.data:
        if item.id == model:
            return item.id
    return models.data[0].id if models.data else model
