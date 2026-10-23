import boto3
import os

def fetch_db_secret(secret_name):
    """
    Fetches a database connection secret from AWS Secrets Manager at runtime.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1") # Example region, can be configured

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
        # Handle exceptions such as ResourceNotFoundException, DecryptionFailureException, etc.
        print(f"Error retrieving secret {secret_name}: {e}")
        raise e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            return get_secret_value_response['SecretBinary']

if __name__ == "__main__":
    # Example usage: Replace 'your_db_secret_name' with your actual secret name in AWS Secrets Manager
    # And ensure AWS_REGION environment variable is set or defaulted correctly.
    try:
        db_secret = fetch_db_secret("your_db_secret_name")
        print("Successfully fetched DB secret (content not shown for security reasons).")
        # In a real application, you would parse db_secret (often JSON) and use it to connect to the database.
        # print(db_secret) # DO NOT print secret in production
    except Exception as e:
        print(f"Failed to fetch DB secret: {e}")
