from __future__ import annotations

from typing import Any, Dict, List

from security_client import build_secret_reference, get_secret_manager_client
from security_models import RotationStatus, summarize_rotation



def rotation_summary(secret_id: str) -> Dict[str, Any]:
    client = get_secret_manager_client()
    ref = build_secret_reference(secret_id=secret_id, version="latest")
    parent = f"projects/{ref.project_id}/secrets/{ref.secret_id}"
    versions: List[RotationStatus] = []
    for item in client.list_secret_versions(request={"parent": parent}):
        versions.append(
            RotationStatus(
                secret_name=parent,
                version=item.name.split("/")[-1],
                state=item.state.name,
                created_time=item.create_time.isoformat() if item.create_time else None,
                destroy_time=item.destroy_time.isoformat() if item.destroy_time else None,
                aliases=list(item.version_aliases),
            )
        )
    summary = summarize_rotation(versions)
    summary["provider"] = "Google Cloud Secret Manager"
    return summary
