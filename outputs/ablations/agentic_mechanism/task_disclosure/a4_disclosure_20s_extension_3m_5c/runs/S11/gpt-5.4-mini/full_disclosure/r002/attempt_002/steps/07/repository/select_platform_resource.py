import os
from typing import Any, Dict, Optional


def select_platform_resource(
    *,
    model: Optional[str] = None,
    deployment: Optional[str] = None,
    inference_profile: Optional[str] = None,
    project: Optional[str] = None,
    location: Optional[str] = None,
) -> Dict[str, Any]:
    provider = "google_vertex_ai"
    resolved_project = project or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    resolved_location = location or os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    resolved_resource = model or deployment or inference_profile or os.getenv("VERTEX_AI_MODEL", "gemini-2.0-flash")
    resource_kind = "model"
    if deployment:
        resource_kind = "deployment"
    elif inference_profile:
        resource_kind = "inference_profile"

    return {
        "provider": provider,
        "project": resolved_project,
        "location": resolved_location,
        "resource_kind": resource_kind,
        "resource": resolved_resource,
        "model": model,
        "deployment": deployment,
        "inference_profile": inference_profile,
        "resource_handle": {
            "provider": provider,
            "project": resolved_project,
            "location": resolved_location,
            "name": resolved_resource,
            "kind": resource_kind,
        },
    }
