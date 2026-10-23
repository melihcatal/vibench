import json
import os
from security_client import get_aws_secrets_manager_client
from security_models import SecretData


def parse_json_secret(secret_name: str) -> SecretData:
    """Retrieves and parses a JSON-formatted secret from AWS Secrets Manager."""
    client = get_aws_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_name}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error fetching secret '{secret_name}': {e}")

    if "SecretString" in get_secret_value_response:
        secret_string = get_secret_value_response["SecretString"]
        try:
            secret_dict = json.loads(secret_string)
            return SecretData(**secret_dict)
        except json.JSONDecodeError as e:
            raise ValueError(f"Secret '{secret_name}' is not a valid JSON: {e}")
        except Exception as e:
            raise ValueError(
                f"Error parsing secret '{secret_name}' into SecretData: {e}"
            )
    else:
        raise TypeError(f"Secret '{secret_name}' did not contain a SecretString.")
