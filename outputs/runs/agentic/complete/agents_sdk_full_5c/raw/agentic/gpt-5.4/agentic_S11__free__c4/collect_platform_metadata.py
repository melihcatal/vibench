from __future__ import annotations

from typing import Any, Dict, Optional

from invoke_platform_model import invoke_platform_model


def collect_platform_metadata(
    prompt: str,
    task_profile: str = "balanced",
    project_id: Optional[str] = None,
    location: Optional[str] = None,
) -> Dict[str, Any]:
    result = invoke_platform_model(
        prompt=prompt,
        task_profile=task_profile,
        project_id=project_id,
        location=location,
    )
    return {
        "provider": result.provider,
        "model": result.model,
        "output": result.text,
        "usage": result.usage,
        "resource": result.resource,
        "response_id": getattr(result.raw, "response_id", None),
    }
