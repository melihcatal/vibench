from model_client import choose_model


def select_platform_resource(preferred_model: str | None = None) -> str:
    return preferred_model or choose_model()
