from __future__ import annotations

from google.cloud import aiplatform_v1

from model_client import load_platform_selection



def select_platform_resource() -> dict[str, str]:
    selection = load_platform_selection()
    client = aiplatform_v1.PublisherModelServiceClient(
        client_options={"api_endpoint": f"{selection.location}-aiplatform.googleapis.com"}
    )
    publisher_model_name = selection.model_resource
    publisher_model = client.get_publisher_model(name=publisher_model_name)
    return {
        "project_id": selection.project_id,
        "location": selection.location,
        "publisher_model": publisher_model.name,
        "version_id": publisher_model.version_id,
        "display_name": publisher_model.display_name,
    }
