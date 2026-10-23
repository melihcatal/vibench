import os
import json
import boto3
from security_client import create_secrets_manager_client
from security_models import normalize_response

# LATER-STEP: Summarize rotation status


def rotation_summary(secret_id: str) -> str:
    """Summarize the rotation status of a secret in AWS Secrets Manager.

    Looks at the secret's version stages and the 'AWSPENDING' label to indicate
    whether rotation has succeeded or is pending.
    """
    client = create_secrets_manager_client()
    # Retrieve the secret details
    secret = client.describe_secret(SecretId=secret_id)
    version_ids = secret.get("VersionIdsToStages", {})
    stages = version_ids.get(secret_id, [])
    if "AWSPENDING" in stages:
        return f"Secret {secret_id} has a pending rotation (AWSPENDING stage)."
    elif "AWSCURRENT" in stages:
        return f"Secret {secret_id} is up-to-date (AWSCURRENT stage)."
    else:
        return f"Secret {secret_id} has an unknown rotation state."
