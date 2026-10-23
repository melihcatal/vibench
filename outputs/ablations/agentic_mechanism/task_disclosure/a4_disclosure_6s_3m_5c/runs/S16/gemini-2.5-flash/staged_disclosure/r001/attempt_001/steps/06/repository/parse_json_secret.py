import boto3
import json
import os

def get_json_secret(secret_name):
    """
    Retrieves and parses a JSON-formatted secret from AWS Secrets Manager.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1") # Use default region if not set

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
    except Exception as e:
        raise Exception(f"Failed to retrieve secret '{secret_name}': {e}")

    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    else:
        raise Exception(f"Secret '{secret_name}' does not contain a SecretString.")

if __name__ == "__main__":
    secret_name = os.environ.get("SECRET_NAME", "my-json-secret") # Default secret name
    try:
        json_secret = get_json_secret(secret_name)
        print(f"Successfully retrieved and parsed secret '{secret_name}':")
        print(json.dumps(json_secret, indent=2))
    except Exception as e:
        print(f"Error: {e}")
