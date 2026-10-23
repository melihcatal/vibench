from model_client import build_platform_client, load_platform_config
from model_models import normalize_messages, response_text, response_usage


def collect_platform_metadata(messages):
    cfg = load_platform_config()
    client = build_platform_client()
    response = client.chat.completions.create(
        model=cfg.deployment,
        messages=normalize_messages(messages),
    )
    return {
        "text": response_text(response),
        "usage": response_usage(response),
        "model": cfg.model,
        "deployment": cfg.deployment,
        "response_id": getattr(response, "id", None),
    }
