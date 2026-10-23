from datetime import datetime, timedelta
from security_client import SecretManagerClient
from security_models import SecretRotationSummaryPayload, RotationSummaryOutput
from google.cloud import secretmanager

def rotation_summary(payload: SecretRotationSummaryPayload) -> list[RotationSummaryOutput]:
    client = SecretManagerClient()
    secrets_summary = []

    parent = f"projects/{payload.project_id}"
    list_secrets_response = client._client.list_secrets(request={"parent": parent})

    for secret in list_secrets_response.secrets:
        secret_id = secret.name.split('/')[-1] # Extract secret_id from name
        
        # List versions for each secret
        list_versions_response = client.list_secret_versions(
            project_id=payload.project_id,
            secret_id=secret_id
        )

        latest_version = None
        latest_create_time = None

        for version in list_versions_response.versions:
            if version.state == secretmanager.SecretVersion.State.ENABLED and version.create_time:
                current_create_time = datetime.fromisoformat(version.create_time.isoformat().replace('Z', '+00:00'))
                if not latest_create_time or current_create_time > latest_create_time:
                    latest_create_time = current_create_time
                    latest_version = version.name.split('/')[-1] # Extract version number
        
        # Determine rotation period (hypothetical, as GCSM doesn't provide it directly)
        # For demonstration, let's assume a default rotation period if not explicitly managed externally
        rotation_period_days = 90 # Example default

        secrets_summary.append(RotationSummaryOutput(
            secret_id=secret_id,
            current_version=latest_version,
            last_rotation=latest_create_time.isoformat() if latest_create_time else None,
            rotation_period_days=rotation_period_days
        ))
    
    return secrets_summary
