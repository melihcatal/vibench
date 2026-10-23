from model_client import resolve_model_id, resolve_resource_id


def select_platform_resource(
    preferred_model: str | None = None, preferred_deployment: str | None = None
) -> dict:
    model_id = preferred_model or resolve_model_id()
    resource_id = resolve_resource_id(preferred_deployment or model_id)
    return {"model_id": model_id, "resource_id": resource_id}
