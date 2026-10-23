
import boto3
import os

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
        return get_secret_value_response['SecretString']
    else:
        return get_secret_value_response['SecretBinary']

if __name__ == "__main__":
    # Replace with your actual secret name
    secret_name = "my_api_key_secret"
    try:
        api_key = get_secret(secret_name)
        print(f"Successfully fetched API key for {secret_name}")
        # In a real application, you would use the api_key here
        # print(f"API Key: {api_key}")
    except Exception as e:
        print(f"Error fetching secret {secret_name}: {e}")
