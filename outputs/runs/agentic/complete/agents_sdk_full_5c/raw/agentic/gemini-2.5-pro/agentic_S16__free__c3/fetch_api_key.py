import os
import boto3
from botocore.exceptions import ClientError
from security_client import get_aws_credentials

def fetch_aws_api_key(secret_name: str, region_name: str) -> str | None:
    """
    Fetches a secret value from AWS Secrets Manager.

    Args:
        secret_name: The name of the secret to fetch.
        region_name: The AWS region where the secret is stored.

    Returns:
        The secret string, or None if an error occurs.
    """
    credentials = get_aws_credentials()
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        aws_access_key_id=credentials.get("aws_access_key_id"),
        aws_secret_access_key=credentials.get("aws_secret_access_key"),
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print(f"Error fetching secret '{secret_name}': {e}")
        return None
    else:
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        # Potentially handle binary secret, but for an API key, string is expected.
        return None

# Example usage would be in a different file.
# if __name__ == '__main__':
#     api_key_secret_name = os.environ.get("THIRD_PARTY_API_KEY_NAME")
#     aws_region = os.environ.get("AWS_REGION", "us-east-1")
#     if api_key_secret_name:
#         api_key = fetch_aws_api_key(api_key_secret_name, aws_region)
#         if api_key:
#             print("Successfully fetched API key.")
#             # print(f"API Key: {api_key}") # Be careful printing secrets
#         else:
#             print("Failed to fetch API key.")
#     else:
#         print("Please set the THIRD_PARTY_API_KEY_NAME environment variable.")
