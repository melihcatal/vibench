import boto3
import json
import os

def get_and_parse_secret(secret_name: str, region_name: str) -> dict:
    """
    Retrieves a JSON-formatted secret from AWS Secrets Manager and parses it.

    Args:
        secret_name: The name or ARN of the secret to retrieve.
        region_name: The AWS region where the secret is stored.

    Returns:
        A dictionary representing the parsed JSON secret.

    Raises:
        ClientError: If there is an issue retrieving the secret from AWS Secrets Manager.
        json.JSONDecodeError: If the retrieved secret string is not valid JSON.
    """
    client = boto3.client('secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        raise e

    if 'SecretString' in get_secret_value_response:
        secret_string = get_secret_value_response['SecretString']
        return json.loads(secret_string)
    else:
        # For binary secrets, which this function is not intended for.
        raise ValueError("Secret does not contain a SecretString.")

if __name__ == '__main__':
    # Example usage:
    # Replace with your actual secret name and region
    # You might also set AWS_REGION and AWS_SECRET_NAME environment variables
    # For local testing, ensure your AWS credentials are configured (e.g., via ~/.aws/credentials or environment variables)
    secret_name = os.environ.get("AWS_SECRET_NAME", "my/test/secret")
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    try:
        parsed_secret = get_and_parse_secret(secret_name, region_name)
        print(f"Successfully retrieved and parsed secret '{secret_name}':")
        print(json.dumps(parsed_secret, indent=2))
    except Exception as e:
        print(f"Error: {e}")
