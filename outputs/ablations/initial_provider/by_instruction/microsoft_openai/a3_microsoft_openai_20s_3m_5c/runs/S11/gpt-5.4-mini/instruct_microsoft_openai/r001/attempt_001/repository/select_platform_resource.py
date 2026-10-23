from model_client import get_default_deployment, get_resource_id


def select_platform_resource() -> dict:
    return {"deployment": get_default_deployment(), "resource_id": get_resource_id()}
