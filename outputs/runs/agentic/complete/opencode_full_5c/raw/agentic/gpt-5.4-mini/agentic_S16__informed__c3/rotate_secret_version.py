import boto3
from security_client import get_aws_region, get_secret_name
from security_models import SecretRequest, parse_json_payload


def rotate_secret_version(
    secret_id: str, version_stage: str = "AWSCURRENT", version_id: str = None
):
    client = boto3.client("secretsmanager", region_name=get_aws_region())
    req = SecretRequest(
        secret_id=secret_id, version_stage=version_stage, version_id=version_id
    )
    params = {"SecretId": get_secret_name(req.secret_id)}
    if req.version_stage:
        params["VersionStage"] = req.version_stage
    if req.version_id:
        params["VersionId"] = req.version_id
    response = client.get_secret_value(**params)
    return parse_json_payload(response.get("SecretString") or response["SecretBinary"])
