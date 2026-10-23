from __future__ import annotations

from security_client import access_secret_value
from security_models import SecretPayload


def fetch_db_secret(
    secret_id: str = "database-connection",
    version_id: str = "latest",
    project_id: str | None = None,
) -> SecretPayload:
    result = access_secret_value(
        secret_id=secret_id, version_id=version_id, project_id=project_id
    )
    return SecretPayload(
        project_id=result["project_id"],
        secret_id=result["secret_id"],
        version_id=result["version_id"],
        value=result["value"],
    )
