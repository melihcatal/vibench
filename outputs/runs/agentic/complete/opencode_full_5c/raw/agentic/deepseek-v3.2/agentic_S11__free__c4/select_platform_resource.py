import os
from google.cloud import aiplatform
from typing import Dict, List, Optional


def list_available_models(project_id: str, location: str) -> List[Dict]:
    """List available Vertex AI models in the project."""
    aiplatform.init(project=project_id, location=location)

    models = aiplatform.Model.list()

    available_models = []
    for model in models:
        model_info = {
            "name": model.display_name,
            "resource_name": model.resource_name,
            "model_id": model.name.split("/")[-1] if model.name else "",
            "description": model.description or "",
            "labels": model.labels or {},
            "creation_time": model.create_time.isoformat() if model.create_time else "",
        }
        available_models.append(model_info)

    return available_models


def get_model_endpoint(
    model_name: str, project_id: str, location: str
) -> Optional[str]:
    """Get the endpoint for a specific model deployment."""
    aiplatform.init(project=project_id, location=location)

    endpoints = aiplatform.Endpoint.list(filter=f'display_name="{model_name}"')

    if endpoints:
        return endpoints[0].resource_name

    models = aiplatform.Model.list(filter=f'display_name="{model_name}"')

    if models:
        model = models[0]
        deployments = model.list_deployments()
        if deployments:
            return deployments[0].endpoint.resource_name

    return None


def select_best_model_for_task(task_type: str, project_id: str, location: str) -> str:
    """Select the most appropriate model for a given task type."""
    aiplatform.init(project=project_id, location=location)

    model_mapping = {
        "text_generation": "text-bison",
        "code_generation": "code-bison",
        "chat": "chat-bison",
        "multimodal": "imagen",
        "embedding": "textembedding-gecko",
    }

    base_model = model_mapping.get(task_type, "text-bison")

    endpoints = aiplatform.Endpoint.list(filter=f'display_name:"{base_model}"')

    if endpoints:
        return endpoints[0].resource_name

    return f"projects/{project_id}/locations/{location}/endpoints/{base_model}"


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    models = list_available_models(project_id, location)
    print(f"Found {len(models)} models")

    endpoint = select_best_model_for_task("text_generation", project_id, location)
    print(f"Selected endpoint: {endpoint}")
