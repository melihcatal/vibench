from model_client import load_platform_config


def select_platform_resource() -> str:
    return load_platform_config().deployment
