from model_client import client


def select_platform_resource() -> str:
    resource_id = client.get_model_id()
    return resource_id
