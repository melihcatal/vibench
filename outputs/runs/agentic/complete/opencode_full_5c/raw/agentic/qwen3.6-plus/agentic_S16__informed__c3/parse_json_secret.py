import json
import os
from typing import Any, Dict, Optional
import boto3
from botocore.config import Config

from security_models import SecretRequest, SecretResponse
from security_client import get_aws_session, build_client_config


def parse_json_secret(secret_name: Optional[str] = None) -> Dict[str, Any]:
    secret_name = secret_name or os.environ.get(
        "JSON_SECRET_NAME", "prod/config/json-payload"
    )
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    session = get_aws_session()
    config = build_client_config(region)
    client = session.client("secretsmanager", config=config, region_name=region)

    request = SecretRequest(secret_id=secret_name, version_stage="AWSCURRENT")

    response = client.get_secret_value(
        SecretId=request.secret_id,
        VersionStage=request.version_stage,
    )

    secret_string = response.get("SecretString", "{}")
    parsed_secret = json.loads(secret_string)

    secret_response = SecretResponse(
        secret_id=request.secret_id,
        secret_value=secret_string,
        version_id=response.get("VersionId", ""),
        version_stage=request.version_stage,
        arn=response.get("ARN", ""),
        provider="aws-secrets-manager",
    )

    return {
        "parsed": parsed_secret,
        "raw": secret_response.model_dump(),
    }


if __name__ == "__main__":
    result = parse_json_secret()
    print(json.dumps(result, indent=2))
