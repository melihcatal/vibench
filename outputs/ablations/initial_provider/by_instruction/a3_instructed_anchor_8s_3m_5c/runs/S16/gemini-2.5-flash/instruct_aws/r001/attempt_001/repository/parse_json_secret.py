import json
from typing import Dict, Any
from security_client import get_secrets_manager_client
from security_models import SecretVersion
import os

def parse_json_secret(secret_name: str) -> Dict[str, Any]:
    """Retrieves and parses a JSON-formatted secret from AWS Secrets Manager."""
    client = get_secrets_manager_client(region_name=os.environ.get('AWS_REGION', 'us-east-1'))
    try:
        response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in response:
            secret_string = response['SecretString']
            return json.loads(secret_string)
        else:
            raise ValueError(f"Secret '{secret_name}' is not a string secret and cannot be parsed as JSON.")
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_name}' not found.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Secret '{secret_name}' is not valid JSON: {e}")
    except Exception as e:
        raise RuntimeError(f"Error parsing JSON secret '{secret_name}': {e}")
