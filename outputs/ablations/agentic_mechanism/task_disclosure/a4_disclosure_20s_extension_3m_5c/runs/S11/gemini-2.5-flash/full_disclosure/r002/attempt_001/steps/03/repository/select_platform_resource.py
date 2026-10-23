from google.cloud import aiplatform

def resolve_model_resource(project_id: str, location: str, model_id: str) -> str:
    """Resolves a Vertex AI model resource name."""
    return aiplatform.models.Model.to_resource_name(project_id, location, model_id)

def resolve_endpoint_resource(project_id: str, location: str, endpoint_id: str) -> str:
    """Resolves a Vertex AI endpoint resource name."""
    return aiplatform.Endpoint.to_resource_name(project_id, location, endpoint_id)
