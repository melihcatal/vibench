from model_client import load_platform_config


def select_platform_resource() -> str:
    config = load_platform_config()
    return config.model
