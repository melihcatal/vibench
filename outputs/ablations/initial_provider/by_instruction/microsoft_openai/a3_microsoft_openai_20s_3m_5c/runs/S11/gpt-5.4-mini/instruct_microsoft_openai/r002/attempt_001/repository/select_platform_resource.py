from model_client import load_platform_config


def select_platform_resource(preferred: str = "") -> str:
    config = load_platform_config()
    return preferred or config.deployment
