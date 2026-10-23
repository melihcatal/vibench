from datetime import datetime


def rotation_summary(
    secret_name: str, fetched_at: str, new_version: str, old_version: str, status: str
) -> str:
    """Summarize secret rotation status.

    Args:
        secret_name: Name of the secret.
        fetched_at: Timestamp when the secret value was retrieved.
        new_version: Version number that was promoted.
        old_version: Previous active version.
        status: 'rotated' or 'failed'.

    Returns:
        A one‑paragraph summary.
    """
    ts = datetime.fromisoformat(fetched_at).strftime("%Y-%m-%d %H:%M:%S")
    summary = (
        f"Secret '{secret_name}' rotation completed at {ts}. "
        f"Promoted version {new_version} and marked obsolete version {old_version}. "
        f"Overall status: {status}."
    )
    return summary
