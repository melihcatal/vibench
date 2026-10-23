from model_client import build_platform_client, load_platform_config
from model_models import normalize_messages


def stream_platform_generation(messages):
    cfg = load_platform_config()
    client = build_platform_client()
    return client.chat.completions.create(
        model=cfg.deployment,
        messages=normalize_messages(messages),
        stream=True,
    )
