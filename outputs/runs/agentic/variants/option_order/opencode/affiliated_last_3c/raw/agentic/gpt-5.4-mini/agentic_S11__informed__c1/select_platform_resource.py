from model_client import deployment_name, get_client, load_config


def select_platform_resource(resource: str | None = None) -> str:
    cfg = load_config()
    return resource or deployment_name(cfg.deployment)


def resolve_platform_model() -> str:
    cfg = load_config()
    return cfg.model


def get_platform_client():
    return get_client()
