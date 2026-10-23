from google.cloud import secretmanager
from datetime import datetime, timedelta, timezone

def summarize_secret_rotation_status(project_id: str, days_since_rotation: int = 90) -> dict:
    """Summarizes secret rotation status for secrets in a given project based on latest version creation time.

    Args:
        project_id: The Google Cloud project ID.
        days_since_rotation: Number of days to consider a secret 'stale' if its latest version is older than this.

    Returns:
        A dictionary summarizing secret rotation status.
    """
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"
    secrets_list = client.list_secrets(request={"parent": parent})

    summary = {
        "total_secrets": 0,
        "stale_secrets": [],
        "active_secrets": []
    }

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_since_rotation)

    for secret in secrets_list:
        summary["total_secrets"] += 1
        secret_name = secret.name
        secret_id = secret_name.split('/')[-1]

        # List versions for the secret to find the latest creation time
        versions = client.list_secret_versions(request={"parent": secret_name})
        latest_version_create_time = None

        # Iterate through versions to find the latest enabled one's creation time
        for version in versions:
            if version.state == secretmanager.SecretVersion.State.ENABLED and version.create_time:
                version_create_time_dt = version.create_time.astimezone(timezone.utc)
                if latest_version_create_time is None or version_create_time_dt > latest_version_create_time:
                    latest_version_create_time = version_create_time_dt
        
        if latest_version_create_time and latest_version_create_time < cutoff_date:
            summary["stale_secrets"].append({"secret_id": secret_id, "last_rotation_approx": latest_version_create_time.isoformat()})
        else:
            summary["active_secrets"].append({"secret_id": secret_id, "last_rotation_approx": latest_version_create_time.isoformat() if latest_version_create_time else "N/A"})

    return summary
