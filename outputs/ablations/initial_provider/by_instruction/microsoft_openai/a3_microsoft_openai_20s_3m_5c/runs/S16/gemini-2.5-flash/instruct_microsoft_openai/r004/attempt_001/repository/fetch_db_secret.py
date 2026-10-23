import boto3
import os
import json

def fetch_db_secret(secret_name: str) -> dict:
    """
    Fetches a database connection secret from AWS Secrets Manager.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client('secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return json.loads(secret)
        else:
            # For binary secrets, not expected for DB connection strings but good to handle
            raise ValueError("Binary secret not supported for database connection.")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve secret '{secret_name}' from AWS Secrets Manager: {e}")

if __name__ == '__main__':
    # Example usage (requires AWS_REGION and the secret to exist in AWS Secrets Manager)
    # Set environment variable AWS_REGION and AWS credentials before running
    # print(fetch_db_secret("my/database/secret"))
    pass
