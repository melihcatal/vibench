from model_client import resource_metadata


def select_platform_resource(model_name: str) -> str:
    return f"azure-openai:{model_name}"


def resolve_resource(model_name: str):
    resource_id = select_platform_resource(model_name)
    return resource_id, resource_metadata(model_name)
