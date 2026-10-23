from __future__ import annotations

from typing import Optional

from model_client import build_selection
from model_models import PlatformSelection


SUPPORTED_VERTEX_MODELS = {
    "balanced": "gemini-1.5-flash",
    "quality": "gemini-1.5-pro",
    "latest-fast": "gemini-2.0-flash-001",
}


def select_platform_resource(
    task_profile: str = "balanced",
    project_id: Optional[str] = None,
    location: Optional[str] = None,
) -> PlatformSelection:
    model_name = SUPPORTED_VERTEX_MODELS.get(task_profile, task_profile)
    return build_selection(model_name=model_name, project_id=project_id, location=location)
