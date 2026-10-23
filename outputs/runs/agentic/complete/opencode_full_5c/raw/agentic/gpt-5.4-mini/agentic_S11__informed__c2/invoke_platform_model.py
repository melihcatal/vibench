from model_client import build_platform_client, load_platform_config
from model_models import normalize_messages, response_text


def invoke_platform_model(messages):
    cfg = load_platform_config()
    client = build_platform_client()
    response = client.chat.completions.create(
        model=cfg.deployment,
        messages=normalize_messages(messages),
    )
    return response_text(response)
