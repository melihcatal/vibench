from fetch_api_key import fetch_api_key
from fetch_db_secret import fetch_db_secret
from parse_json_secret import parse_json_secret
from rotate_secret_version import rotate_secret_version

SUMMARY_HEADER = "=== Secret Rotation Summary ==="


def rotation_summary(secret_id: str) -> str:
    """Generate a concise report of the secret's current version and a rotated version if available."""
    current = rotate_secret_version(secret_id, version_stage="AWSCURRENT")
    latest = rotate_secret_version(secret_id, version_stage="AWSPREVIOUS")
    lines = [
        SUMMARY_HEADER,
        f"Secret ID: {secret_id}",
        f"Current Version: {current.get('VersionId')}",
    ]
    if latest:
        lines.append(f"Latest (Previous) Version: {latest.get('VersionId')}")
    return "\\n".join(lines)
