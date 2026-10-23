from typing import Optional, Dict, Any
import os
from google.cloud import aiplatform


def select_vertex_resource(
    project_id: str,
    location: str,
    model_display_name: Optional[str] = None,
    model_id: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Resolves a Vertex AI model or deployment resource by display name or ID.
    Returns the model resource dictionary including model ID, display name, and endpoint.
    """
    if credentials_path:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        aiplatform.init(project=project_id, location=location, credentials=credentials)
    else:
        aiplatform.init(project=project_id, location=location)

    if model_id:
        model = aiplatform.Model(
            model_name=f"projects/{project_id}/locations/{location}/models/{model_id}"
        )
        return {
            "model_id": model.resource_name.split("/")[-1],
            "display_name": model.display_name,
            "model_resource_name": model.resource_name,
            "endpoint": model.deployed_endpoints[0].resource_name
            if model.deployed_endpoints
            else None,
        }
    elif model_display_name:
        models = aiplatform.Model.list(filter=f"display_name={model_display_name}")
        if not models:
            raise ValueError(f"No model found with display name: {model_display_name}")
        model = models[0]
        return {
            "model_id": model.resource_name.split("/")[-1],
            "display_name": model.display_name,
            "model_resource_name": model.resource_name,
            "endpoint": model.deployed_endpoints[0].resource_name
            if model.deployed_endpoints
            else None,
        }
    else:
        raise ValueError("Either model_display_name or model_id must be provided")
