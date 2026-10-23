# rotation_summary.py
import json
from security_models import SecretReadResponse
from security_client import get_secret_manager_client

def rotation_summary(secret_name: str) -> str:
    """Summarize the rotation status of a secret.

    Uses AWS Secrets Manager to inspect the current version and its stage labels.
    Returns a human‑readable summary string.
    """
    client = get_secret_manager_client()
    response = client.describe_secret(SecretId=secret_name)
    metadata = response['ARN'], response['Name'], response['Description']
    current_version = response['VersionIdsToStages'][list(response['VersionIdsToStages'].keys())[0]]

    summary = f"Secret '{secret_name}' (ARN: {metadata[0]})\n"
    summary += f"Current version: {response['LatestVersionNumber']}\n"
    summary += "Stages attached to versions:\n"
    for ver, stages in response['VersionIdsToStages'].items():
        stage_str = ', '.join(stages) if stages else 'none'
        summary += f"  version {ver}: {stage_str}\n"
    return summary
```