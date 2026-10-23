from __future__ import annotations

from typing import Optional

from google.cloud import aiplatform_v1

from model_client import get_location, get_project_id
from model_models import PlatformSelection



def resolve_platform_resource(
    model_name: Optional[str] = None,
    project_id: Optional[str] = None,
    location: Optional[str] = None,
) -> PlatformSelection:
    resolved_project = get_project_id(project_id)
    resolved_location = get_location(location)
    publisher_model = model_name or "gemini-1.5-pro"

    client = aiplatform_v1.PublisherModelServiceClient(
        client_options={"api_endpoint": f"{resolved_location}-aiplatform.googleapis.com"}
    )
    resource_name = client.publisher_model_path(
        project=resolved_project,
        location=resolved_location,
        publisher="google",
        model=publisher_model,
    )
    client.get_publisher_model(name=resource_name)
    return PlatformSelection(
        project_id=resolved_project,
        location=resolved_location,
        publisher="google",
        model=publisher_model,
    )
