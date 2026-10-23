import os
import json
from typing import Any, Dict
from security_models import SecretResponse, SecretMetadata, ParsedSecretResponse
from security_client import get_aws_client, handle_aws_error


def parse_json_secret(secret_name: str, region: str = None) -> ParsedSecretResponse:
    client = get_aws_client(region)
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret_value = response.get("SecretString", "")
        version_id = response.get("VersionId", "")
        arn = response.get("ARN", "")
        name = response.get("Name", secret_name)
        parsed_data: Dict[str, Any] = json.loads(secret_value)
        metadata = SecretMetadata(
            secret_id=version_id,
            arn=arn,
            name=name,
        )
        return ParsedSecretResponse(
            secret_value=secret_value,
            parsed_data=parsed_data,
            metadata=metadata,
            provider="AWS Secrets Manager",
        )
    except json.JSONDecodeError as e:
        raise ValueError(f"Secret '{secret_name}' is not valid JSON: {e}")
    except Exception as e:
        raise handle_aws_error(e, secret_name)


if __name__ == "__main__":
    secret_name = os.environ.get("AWS_JSON_SECRET_NAME", "production/config-json")
    result = parse_json_secret(secret_name)
    print(json.dumps(result.to_dict(), indent=2))
