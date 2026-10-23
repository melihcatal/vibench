import boto3
import os
from security_models import SecretRequest, SecretResponse

def rotate_secret_version(req: SecretRequest) -> SecretResponse:
    client = boto3.client(
        "secretsmanager",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    )
    kwargs = {"SecretId": req.name}
    if req.version:
        kwargs["VersionId"] = req.version
    else:
        kwargs["VersionStage"] = "AWSPENDING"
    resp = client.get_secret_value(**kwargs)
    return SecretResponse(value=resp["SecretString"], version=resp["VersionId"])