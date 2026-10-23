import os
import json
import boto3
from botocore.exceptions import ClientError
from security_client import get_client_config
from security_models import normalize_response, NormalizedSecret, SecretRequest


def rotate_secret_version(request: SecretRequest) -> NormalizedSecret:
    """Read a specific secret version or staged value from AWS Secrets Manager.

    Args:
        request: A SecretRequest instance with name and optional version/staged flag.

    Returns:
        A NormalizedSecret with unified fields.
    """
    secret_name = request["name"]
    secrets_client = boto3.client("secretsmanager", region_name=os.getenv("AWS_REGION"))
    kwargs = {"SecretId": secret_name}
    if request.get("version"):
        kwargs["VersionStage"] = "AWSCURRENT"  # can also use version ID if needed
    try:
        response = secrets_client.get_secret_value(**kwargs)
    except ClientError as e:
        raise RuntimeError(f"Error fetching secret: {e}")
    # Build unified normalized secret
    normalized = {
        "provider": "aws",
        "name": secret_name,
        "value": response["SecretString"]
        or base64.b64decode(response["SecretBinary"]).decode("utf-8"),
        "metadata": {
            "name": secret_name,
            "description": response.get("Description"),
            "created_at": response.get("CreationDate", "").isoformat()
            if response.get("CreationDate")
            else None,
        },
    }
    return normalize_response("aws", normalized)
