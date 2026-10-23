from security_client import build_secrets_client, normalize_secret_name
from security_models import SecretRequest, SecretVersionResult


def rotate_secret_version(secret_id: str, version_stage: str = "AWSPENDING") -> SecretVersionResult:
    client = build_secrets_client()
    request = SecretRequest(secret_id=secret_id, version_stage=version_stage)
    response = client.get_secret_value(SecretId=normalize_secret_name(request.secret_id), VersionStage=request.version_stage)
    return SecretVersionResult.from_aws_secret(response)
