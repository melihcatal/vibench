from google.cloud import aiplatform


def resolve_vertex_ai_resource_name(
    project_id: str,
    location: str,
    resource_id: str,
    resource_type: str,  # "endpoint" or "model"
) -> str:
    if resource_type == "endpoint":
        return aiplatform.PredictionServiceClient.endpoint_path(
            project=project_id, location=location, endpoint=resource_id
        )
    elif resource_type == "model":
        return aiplatform.PredictionServiceClient.model_path(
            project=project_id, location=location, model=resource_id
        )
    else:
        raise ValueError("resource_type must be 'endpoint' or 'model'")
