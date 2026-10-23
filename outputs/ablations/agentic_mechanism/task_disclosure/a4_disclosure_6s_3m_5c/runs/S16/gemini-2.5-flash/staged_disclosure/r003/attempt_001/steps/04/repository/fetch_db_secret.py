import boto3
import os
import json

def get_secret(secret_name):
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
    except Exception as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if 'SecretString' in get_secret_value_response:
        return json.loads(get_secret_value_response['SecretString'])
    else:
        return get_secret_value_response['SecretBinary']

if __name__ == "__main__":
    # Replace "YOUR_SECRET_NAME" with the actual name of your secret in AWS Secrets Manager
    secret = get_secret(os.environ.get("DB_SECRET_NAME", "YOUR_SECRET_NAME"))
    print("Fetched secret (partial view):", {k: v for k, v in secret.items() if k not in ["password", "token"]}) # Print sensitive info partially
