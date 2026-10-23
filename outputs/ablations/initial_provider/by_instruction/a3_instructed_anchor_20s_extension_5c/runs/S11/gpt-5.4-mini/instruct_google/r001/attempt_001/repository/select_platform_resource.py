from model_client import get_model_name


def select_platform_resource(preferred: str = None) -> str:
    return preferred or get_model_name()
