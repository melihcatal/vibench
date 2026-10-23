import os
import boto3
from botocore.exceptions import ClientError

def get_api_key(secret_name: str) -> str:
    """Fetches an API key from AWS Secrets Manager."""
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e
    
    # Decrypts secret using the associated KMS key.
    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if 'SecretString' in get_secret_value_response:
        return get_secret_value_response['SecretString']
    else:
        # Binary secrets are base64 encoded, but Secrets Manager SDK handles the decoding
        return get_secret_value_response['SecretBinary'].decode('utf-8')

if __name__ == '__main__':
    # Example usage (requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION env vars)
    # api_key = get_api_key("my-api-key-secret")
    # print(f"Fetched API Key: {api_key}")
    pass
