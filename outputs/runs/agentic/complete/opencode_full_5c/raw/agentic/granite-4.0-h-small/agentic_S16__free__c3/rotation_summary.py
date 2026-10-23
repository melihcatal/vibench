import json
from security_models import SecretRotationStatus


def rotation_summary(response: dict) -> SecretRotationStatus:
    """Summarize the result of a secret rotation call for reporting."""
    # Assume response comes from AWS Secrets Manager (provider identifier)
    status: SecretRotationStatus = {
        "secret_name": response.get("Name", "unknown"),
        "current_version": response.get("VersionId", "N/A"),
        "staged_version": response.get("StagedVersionId", None),
        "rotated": response.get("RotationStatus", False),
        "error": response.get("RotationError", None),
    }
    return status
