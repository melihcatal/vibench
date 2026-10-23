from model_client import get_platform_deployment

def select_platform_resource(model_family: str) -> str:
    """Resolves Azure OpenAI deployment name for the model family."""
    return get_platform_deployment(model_family)
