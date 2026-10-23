from __future__ import annotations

from google.cloud import secretmanager

from security_client import (
    DEFAULT_PROVIDER,
    get_gcp_project_id,
    parse_version_from_name,
    secret_manager_client,
)
from security_models import SecretValue, SecretVersionSelection, normalize_secret_text


def read_secret_version(
    secret_id: str,
    project_id: str | None = None,
    version_id: str | None = None,
    stage: str | None = None,
) -> SecretValue:
    selection = SecretVersionSelection(
        project_id=get_gcp_project_id(project_id),
        secret_id=secret_id,
        version_id=version_id,
        stage=stage,
    )
    client = secret_manager_client()
    if selection.version_id:
        name = f"projects/{selection.project_id}/secrets/{selection.secret_id}/versions/{selection.version_id}"
        response = client.access_secret_version(request={"name": name})
    elif selection.stage:
        parent = f"projects/{selection.project_id}/secrets/{selection.secret_id}"
        versions = client.list_secret_versions(
            request={
                "parent": parent,
                "filter": f"state:{secretmanager.SecretVersion.State.ENABLED.name}",
            }
        )
        matched = None
        for version in versions:
            aliases = set(version.version_aliases)
            if selection.stage in aliases:
                matched = client.access_secret_version(request={"name": version.name})
                break
        if matched is None:
            raise ValueError(
                f"No Google Secret Manager version alias matched {selection.stage}"
            )
        response = matched
    else:
        response = client.access_secret_version(
            request={
                "name": f"projects/{selection.project_id}/secrets/{selection.secret_id}/versions/latest"
            }
        )
    return SecretValue(
        provider=DEFAULT_PROVIDER,
        resource_name=response.name,
        value=normalize_secret_text(response.payload.data),
        version=parse_version_from_name(response.name),
    )
