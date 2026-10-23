import boto3
import os
import json

def get_secret(secret_name: str, region_name: str = 'us-east-1'):
    """
    Fetches a database connection secret from AWS Secrets Manager at runtime.

    Args:
        secret_name: The name of the secret to retrieve.
        region_name: The AWS region where the secret is stored.

    Returns:
        The retrieved secret string.
    """
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
        # For a clean exit, catch the exception and print the error message.
        print(f"Error retrieving secret '{secret_name}': {e}")
        return None

    # Decrypts secret using the associated KMS key.
    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if 'SecretString' in get_secret_value_response:
        return get_secret_value_response['SecretString']
    else:
        return get_secret_value_response['SecretBinary']

if __name__ == '__main__':
    # Example usage:
    # Set the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables
    # or configure your AWS credentials in ~/.aws/credentials
    # and ~/.aws/config files.
    # Replace 'your/secret/name' with the actual name of your secret in AWS Secrets Manager.
    # Replace 'your-aws-region' with your AWS region, e.g., 'us-west-2'.
    
    # You would typically get the secret name from an environment variable or configuration
    secret_name_example = os.environ.get("DB_SECRET_NAME", "your/secret/name")
    aws_region_example = os.environ.get("AWS_REGION", "us-east-1")

    db_secret = get_secret(secret_name_example, aws_region_example)

    if db_secret:
        print("Successfully retrieved the database secret.")
        # If the secret is a JSON string, you might want to parse it
        try:
            secret_dict = json.loads(db_secret)
            print(f"Database username: {secret_dict.get('username')}")
            # Do not print the full secret for security reasons in a real application
            # print(f"Full secret: {db_secret}")
        except json.JSONDecodeError:
            print(f"Secret is not a JSON string: {db_secret}")
    else:
        print("Failed to retrieve the database secret.")
