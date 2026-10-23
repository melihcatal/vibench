
import boto3
import json
import os

def get_and_parse_json_secret(secret_name):
    """
    Retrieves and parses a JSON-formatted secret from AWS Secrets Manager.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1") # Example AWS region

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
        print(f"Error retrieving secret '{secret_name}': {e}")
        raise

    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    else:
        # For binary secrets, we would decode them here.
        # This example assumes a string secret.
        raise ValueError("SecretString not found in the response.")

if __name__ == "__main__":
    # Replace 'YOUR_SECRET_NAME' with the actual name of your secret in AWS Secrets Manager
    # Ensure AWS_REGION environment variable is set or modify the default region_name
    # Ensure you have AWS credentials configured (e.g., via AWS CLI or environment variables)
    aws_secret_name = os.environ.get("AWS_SECRET_NAME", "your/secret/name")

    try:
        parsed_secret = get_and_parse_json_secret(aws_secret_name)
        print("Successfully retrieved and parsed secret:")
        print(json.dumps(parsed_secret, indent=2))
    except Exception as e:
        print(f"Failed to process secret: {e}")
