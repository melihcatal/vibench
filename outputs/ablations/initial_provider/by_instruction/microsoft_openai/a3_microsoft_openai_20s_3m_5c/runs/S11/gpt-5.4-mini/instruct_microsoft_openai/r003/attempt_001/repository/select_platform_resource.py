from model_client import build_platform_client, load_platform_config


def select_platform_resource(preferred_deployment: str | None = None) -> str:
    config = load_platform_config()
    client = build_platform_client(config)
    _ = client
    return preferred_deployment or config.deployment
