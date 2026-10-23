import os
import json
import boto3
from botocore.exceptions import ClientError


def parse_json_secret(secret_name):
    """
    Retrieve and parse a JSON-formatted secret from AWS Secrets Manager.
    Returns the parsed JSON data as a dictionary.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response:
            secret_string = response["SecretString"]
            parsed_data = json.loads(secret_string)
            return parsed_data
        else:
            raise ValueError("Secret is not in string format")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            raise Exception(f"JSON secret {secret_name} not found")
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            raise Exception(f"Invalid request for JSON secret {secret_name}")
        else:
            raise Exception(f"Error fetching JSON secret: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON secret {secret_name}: {e}")
