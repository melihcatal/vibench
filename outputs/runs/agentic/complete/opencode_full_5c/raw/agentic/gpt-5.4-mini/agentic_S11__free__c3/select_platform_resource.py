from model_client import (
    get_client,
    get_deployment_name,
    get_model_name,
    get_provider_name,
)


def select_platform_resource(preferred: str = None):
    provider = get_provider_name().lower()
    client = get_client()
    if provider == "azure":
        return client, get_deployment_name()
    return client, preferred or get_model_name()
