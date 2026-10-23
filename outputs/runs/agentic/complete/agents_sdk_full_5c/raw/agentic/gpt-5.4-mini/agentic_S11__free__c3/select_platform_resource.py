from typing import Optional

from openai import OpenAI

from model_client import build_client, load_config


def resolve_platform_resource(preferred_model: Optional[str] = None) -> str:
    config = load_config()
    client: OpenAI = build_client(config)
    model_id = preferred_model or config.model
    models = client.models.list()
    available = {m.id for m in models.data}
    if model_id in available:
        return model_id
    for candidate in ("gpt-4.1-mini", "gpt-4.1", "gpt-4o-mini"):
        if candidate in available:
            return candidate
    raise LookupError("No supported OpenAI model resource found")


if __name__ == "__main__":
    print(resolve_platform_resource())
