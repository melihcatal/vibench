from typing import Dict, Optional
import os
import json
import boto3
from botocore.exceptions import ClientError


def parse_json_secret(secret_name: str) -> Optional[Dict]:
    """
    Retrieves and parses a JSON-formatted secret from AWS Secrets Manager.
    """
    region_name = os.getenv("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret_value = response.get("SecretString")

        if secret_value:
            return json.loads(secret_value)
        return None
    except ClientError as e:
        print(f"Failed to fetch or parse JSON secret: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON secret: {e}")
        return None
