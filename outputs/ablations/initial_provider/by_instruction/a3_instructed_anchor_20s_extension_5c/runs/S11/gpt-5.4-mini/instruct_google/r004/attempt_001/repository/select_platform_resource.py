from google.cloud import aiplatform

from model_client import init_vertex_ai


def select_platform_resource(resource_id: str | None = None) -> str:
    config = init_vertex_ai()
    if resource_id:
        return resource_id
    endpoint = aiplatform.Endpoint.list(filter=f'display_name="{config.model_name}"', order_by="create_time desc", project=config.project, location=config.location)
    if endpoint:
        return endpoint[0].resource_name
    return config.model_name
