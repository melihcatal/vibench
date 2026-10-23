import os
import json
from security_client import get_aws_secrets_manager_client
from security_models import SecretRequest, JsonSecret


def parse_json_secret(request: SecretRequest) -> JsonSecret:
    client = get_aws_secrets_manager_client()
    response = client.get_secret_value(
        SecretId=request.secret_name,
        VersionId=request.version_id if request.version_id else "DEFAULT",
        VersionStage=request.version_stage if request.version_stage else "AWSCURRENT",
    )
    secret_string = response["SecretString"]
    return JsonSecret(**json.loads(secret_string))
