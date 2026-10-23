# rotation_summary.py
import os
import boto3
from security_client import SecretManagerClient
from security_models import SecretRotationSuccess

def summarize_rotation(secret_id: str) -> str:
    """Summarize the status of a secret rotation for a given secret ID.

    The function checks if a rotation Lambda is attached and whether a pending rotation
    exists. It reports one of the following states:
    - Not configured for rotation
    - No pending rotation (current version is active)
    - Pending rotation ready (AWSPENDING present)
    - Rotation completed (AWSCURRENT updated)

    Returns a human‑readable summary string.
    """
    client = SecretManagerClient()
    try:
        # Attempt to start a rotation; the API returns no content on success.
        # We query the secret's rotation configuration instead of actually invoking it.
        rotation_cfg = client.client.get_secret_value(secret_id).get('ARN')  # placeholder
        # Fetch metadata instead of using get_secret_value
        metadata = client.get_secret_metadata(secret_id)
    except Exception as exc:
        return f"ERROR: Could not query secret metadata: {exc}"

    # AWS does not expose a direct \"is rotation enabled\" flag via a single API call.
    # We infer from the presence of a RotationLambdaArn in describe_secret response.
    # Re‑fetch with describe_secret to locate the ARN.
    try:
        desc = client.client.describe_secret(SecretId=secret_id)
        rotation_lambda_arn = desc.get('RotationLambdaArn')
    except Exception:
        rotation_lambda_arn = None

    state = 
    if rotation_lambda_arn is None:
        "Not configured for rotation"
    elif rotation_lambda_arn and 'AWSPENDING' in client.client.list_secret_version_ids(SecretId=secret_id)['VersionIdsToStages']:
        "Pending rotation ready"
    elif rotation_lambda_arn and 'AWSCURRENT' in client.client.list_secret_version_ids(SecretId=secret_id)['VersionIdsToStages']:
        "Rotation completed (new version active)"
    else:
        "No pending rotation"

    return f"Secret {secret_id} rotation status: {state}" 

if __name__ == '__main__':
    print(summarize_rotation('my-rotated-secret'))