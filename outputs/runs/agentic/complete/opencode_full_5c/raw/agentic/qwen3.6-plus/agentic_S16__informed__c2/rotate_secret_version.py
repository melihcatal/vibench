import os
import json
from security_models import SecretResponse, SecretMetadata
from security_client import get_aws_client, handle_aws_error


def rotate_secret_version(
    secret_name: str,
    version_stage: str = "AWSCURRENT",
    version_id: str = None,
    region: str = None,
) -> SecretResponse:
    client = get_aws_client(region)
    try:
        if version_id:
            response = client.get_secret_value(
                SecretId=secret_name,
                VersionId=version_id,
                VersionStage=version_stage,
            )
        else:
            response = client.get_secret_value(
                SecretId=secret_name,
                VersionStage=version_stage,
            )
        secret_value = response.get("SecretString", "")
        returned_version_id = response.get("VersionId", "")
        arn = response.get("ARN", "")
        name = response.get("Name", secret_name)
        metadata = SecretMetadata(
            secret_id=returned_version_id,
            arn=arn,
            name=name,
        )
        return SecretResponse(
            secret_value=secret_value,
            metadata=metadata,
            provider="AWS Secrets Manager",
        )
    except Exception as e:
        raise handle_aws_error(e, secret_name)


if __name__ == "__main__":
    secret_name = os.environ.get(
        "AWS_ROTATION_SECRET_NAME", "production/rotating-secret"
    )
    version_stage = os.environ.get("AWS_VERSION_STAGE", "AWSCURRENT")
    result = rotate_secret_version(secret_name, version_stage=version_stage)
    print(json.dumps(result.to_dict(), indent=2))
