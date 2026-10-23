import os
from security_client import get_aws_secrets_manager_client
from security_models import SecretRequest, SecretResponse


def fetch_api_key(request: SecretRequest) -> SecretResponse:
    client = get_aws_secrets_manager_client()
    response = client.get_secret_value(
        SecretId=request.secret_name,
        VersionId=request.version_id if request.version_id else "DEFAULT",
        VersionStage=request.version_stage if request.version_stage else "AWSCURRENT",
    )
    return SecretResponse(
        name=response["Name"],
        arn=response["ARN"],
        secret_string=response["SecretString"],
        created_date=float(response["CreatedDate"].timestamp()),
        version_id=response["VersionId"],
    )
