from typing import Optional
from security_models import SecretRequest, SecretType, RotationStatus
from security_client import get_vault_client


def read_secret_version(
    secret_path: str, version: int, mount_point: Optional[str] = None
) -> dict:
    client = get_vault_client()
    try:
        response = client.read_secret_version(secret_path, version, mount_point)
        return {
            "version": response.version,
            "value": response.value,
            "created_time": response.created_time,
            "rotation_status": _determine_rotation_status(response, version),
        }
    finally:
        client.close()


def read_staged_secret(
    secret_path: str, mount_point: Optional[str] = None
) -> Optional[dict]:
    client = get_vault_client()
    try:
        metadata = client.get_rotation_info(secret_path, mount_point)
        versions = metadata.get("versions", {})
        for ver_num, ver_info in sorted(
            versions.items(), key=lambda x: int(x[0]), reverse=True
        ):
            if ver_info.get("status") == "staged":
                return {
                    "version": int(ver_num),
                    "created_time": ver_info.get("created_time"),
                    "status": "staged",
                }
        return None
    finally:
        client.close()


def _determine_rotation_status(response, requested_version: int) -> str:
    metadata = response.metadata
    current_version = metadata.get("version")
    if current_version is None:
        return RotationStatus.ACTIVE.value
    if requested_version == current_version:
        return RotationStatus.ACTIVE.value
    if requested_version < current_version:
        return RotationStatus.ROTATED.value
    return RotationStatus.PENDING.value


if __name__ == "__main__":
    import os

    secret_path = os.environ.get("VERSIONED_SECRET_PATH", "prod/certs/tls-cert")
    version = int(os.environ.get("SECRET_VERSION", "1"))
    result = read_secret_version(secret_path, version)
    print(result)
