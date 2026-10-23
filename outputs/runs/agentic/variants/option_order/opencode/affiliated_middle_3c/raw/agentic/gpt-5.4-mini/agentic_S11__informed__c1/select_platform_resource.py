from model_client import (
    resolve_model_name,
    resolve_deployment_id,
    resolve_platform_resource,
)


def select_platform_resource(
    model: str = None, deployment: str = None, resource: str = None
):
    selected = resolve_platform_resource(
        resource=resource, model=model, deployment=deployment
    )
    return {
        "resource": selected,
        "model": resolve_model_name(model),
        "deployment": resolve_deployment_id(deployment),
    }
