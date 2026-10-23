import boto3
import json
import os

def get_and_parse_json_secret(secret_name: str, region_name: str = 'us-east-1'):
    """
    Retrieves and parses a JSON-formatted secret from AWS Secrets Manager.

    Args:
        secret_name: The name of the secret to retrieve.
        region_name: The AWS region where the secret is stored.

    Returns:
        A dictionary representing the parsed JSON secret.
    Raises:
        ClientError: If there is an error retrieving the secret.
        json.JSONDecodeError: If the secret string is not valid JSON.
    """
    client = boto3.client('secretsmanager', region_name=region_name)
    
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        raise Exception(f"Failed to retrieve secret '{secret_name}': {e}")

    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        # For binary secrets, which is not the primary use case here, but good to handle
        raise ValueError("SecretString not found in the response. This function expects a JSON string secret.")

    return json.loads(secret)

if __name__ == '__main__':
    # Example usage:
    # Set the secret name and region. You would typically get these from environment variables
    # or a configuration file in a real application.
    # Ensure AWS credentials are configured in your environment (e.g., via AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN
    # or ~/.aws/credentials file).
    
    # Replace 'YOUR_SECRET_NAME' with the actual name of your JSON secret in AWS Secrets Manager.
    # Replace 'YOUR_AWS_REGION' with the AWS region where your secret is located, e.g., 'us-east-1'.
    
    SECRET_NAME = os.getenv('MY_JSON_SECRET_NAME', 'YOUR_SECRET_NAME')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

    if SECRET_NAME == 'YOUR_SECRET_NAME':
        print("Please set the 'MY_JSON_SECRET_NAME' environment variable or modify the script with your secret name.")
    else:
        try:
            parsed_secret = get_and_parse_json_secret(SECRET_NAME, AWS_REGION)
            print(f"Successfully retrieved and parsed secret '{SECRET_NAME}':")
            print(json.dumps(parsed_secret, indent=2))
        except Exception as e:
            print(f"Error: {e}")
