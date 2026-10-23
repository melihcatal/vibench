import os
import json
from security_models import SecretResponse, SecretMetadata
from security_client import get_aws_client, handle_aws_error


def fetch_api_key(secret_name: str, region: str = None) -> SecretResponse:
    client = get_aws_client(region)
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret_value = response.get("SecretString", "")
        version_id = response.get("VersionId", "")
        arn = response.get("ARN", "")
        name = response.get("Name", secret_name)
        metadata = SecretMetadata(
            secret_id=version_id,
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
    secret_name = os.environ.get("AWS_SECRET_NAME", "production/api-key")
    result = fetch_api_key(secret_name)
    print(json.dumps(result.to_dict(), indent=2))
