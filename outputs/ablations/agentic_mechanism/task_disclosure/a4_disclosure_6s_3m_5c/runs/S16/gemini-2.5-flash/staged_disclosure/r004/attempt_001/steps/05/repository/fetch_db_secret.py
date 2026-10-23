import boto3
import os

def get_db_secret(secret_name):
    """
    Fetches a database connection secret from AWS Secrets Manager at runtime.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1") # Example region, can be configured

    # Create a Secrets Manager client
    client = boto3.client('secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        # Handle exceptions such as ResourceNotFoundException, DecryptionFailureException, etc.
        print(f"Error retrieving secret '{secret_name}': {e}")
        raise e

    # Decrypts secret using the associated KMS CMK.
    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if 'SecretString' in get_secret_value_response:
        return get_secret_value_response['SecretString']
    else:
        return get_secret_value_response['SecretBinary'].decode('utf-8')

if __name__ == "__main__":
    # Replace 'your/secret/name' with the actual name of your secret in AWS Secrets Manager
    # It's recommended to load this from an environment variable or configuration in a real application.
    SECRET_NAME = os.environ.get("DB_SECRET_NAME", "your/secret/name")

    try:
        db_secret = get_db_secret(SECRET_NAME)
        print(f"Successfully fetched secret for '{SECRET_NAME}'.")
        # In a real application, you would parse the JSON string and use the credentials
        # For example:
        # import json
        # secret_dict = json.loads(db_secret)
        # print(f"Username: {secret_dict.get('username')}")
        # print(f"Password: {secret_dict.get('password')}")
    except Exception:
        print(f"Failed to fetch secret '{SECRET_NAME}'. See error details above.")
