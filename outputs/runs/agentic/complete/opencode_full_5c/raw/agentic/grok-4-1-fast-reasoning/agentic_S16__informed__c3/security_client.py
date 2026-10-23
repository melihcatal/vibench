import os
import boto3
from botocore.exceptions import ClientError
from security_models import SecretRequest, SecretResponse, parse_secret_response


def get_secrets_client():
    return boto3.client(
        "secretsmanager", region_name=os.getenv("AWS_REGION", "us-east-1")
    )


def fetch_secret(req: SecretRequest) -> SecretResponse:
    client = get_secrets_client()
    kwargs = {"SecretId": req.name}
    if req.version_id is not None:
        kwargs["VersionId"] = req.version_id
    if req.version_stage is not None:
        kwargs["VersionStage"] = req.version_stage
    try:
        raw_resp = client.get_secret_value(**kwargs)
        return parse_secret_response(raw_resp)
    except ClientError as e:
        raise RuntimeError(f"Error fetching secret {req.name}: {str(e)}")
