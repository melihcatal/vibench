from model_client import get_platform_client, load_platform_config


def collect_platform_metadata(prompt: str) -> dict:
    cfg = load_platform_config()
    client = get_platform_client()
    response = client.chat.completions.create(
        model=cfg.model, messages=[{"role": "user", "content": prompt}]
    )
    return {
        "text": response.choices[0].message.content or "",
        "model": cfg.model,
        "usage": getattr(response, "usage", None),
        "resource_id": getattr(response, "id", ""),
    }
