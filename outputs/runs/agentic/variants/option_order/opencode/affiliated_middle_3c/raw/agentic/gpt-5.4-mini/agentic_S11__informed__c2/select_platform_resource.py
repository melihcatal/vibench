from model_client import load_platform_config


def select_platform_resource(name: str | None = None) -> str:
    cfg = load_platform_config()
    return name or cfg.model
