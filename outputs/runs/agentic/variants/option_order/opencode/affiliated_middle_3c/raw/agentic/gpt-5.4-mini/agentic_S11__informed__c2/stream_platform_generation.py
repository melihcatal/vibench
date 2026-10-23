from model_client import get_platform_client, load_platform_config


def stream_platform_generation(prompt: str):
    cfg = load_platform_config()
    client = get_platform_client()
    return client.chat.completions.create(
        model=cfg.model, messages=[{"role": "user", "content": prompt}], stream=True
    )
