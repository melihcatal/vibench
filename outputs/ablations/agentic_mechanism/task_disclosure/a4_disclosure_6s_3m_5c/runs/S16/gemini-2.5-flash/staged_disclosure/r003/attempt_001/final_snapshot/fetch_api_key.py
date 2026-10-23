import boto3
import os

def get_secret(secret_name):
    region_name = os.environ.get("AWS_REGION", "us-east-1") # Replace with your desired AWS region

    # Create a Secrets Manager client
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        print(f"Error fetching secret: {e}")
        return None
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if "SecretString" in get_secret_value_response:
            return get_secret_value_response["SecretString"]
        else:
            return get_secret_value_response["SecretBinary"]

if __name__ == "__main__":
    # Replace "your/secret/name" with the actual name of your secret in AWS Secrets Manager
    api_key = get_secret("your/secret/name")
    if api_key:
        print(f"Successfully fetched API Key (first 5 chars): {api_key[:5]}...")
    else:
        print("Failed to fetch API Key.")
