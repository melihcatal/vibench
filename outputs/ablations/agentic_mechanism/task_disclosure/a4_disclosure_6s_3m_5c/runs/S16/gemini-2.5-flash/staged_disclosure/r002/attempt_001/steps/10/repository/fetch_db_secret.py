import boto3
import os

def get_db_secret(secret_name):
    """
    Fetches a database connection secret from AWS Secrets Manager at runtime.
    
    Args:
        secret_name (str): The name of the secret to retrieve.
        
    Returns:
        str: The retrieved secret string.
    """
    
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=os.environ.get('AWS_REGION', 'us-east-1') # Default to us-east-1, but can be overridden by env var
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        # Handle exceptions such as ResourceNotFoundException or DecryptionFailureException
        print(f"Error retrieving secret '{secret_name}': {e}")
        raise e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            return get_secret_value_response['SecretBinary'].decode('utf-8')

if __name__ == "__main__":
    # Replace 'your/secret/name' with the actual name of your secret in AWS Secrets Manager
    # Example: 'prod/db/credentials' or 'my-application-secrets/db-password'
    secret_name = os.environ.get('DB_SECRET_NAME', 'your/secret/name') 

    try:
        db_secret = get_db_secret(secret_name)
        print(f"Successfully fetched secret for '{secret_name}'.")
        # In a real application, you would parse db_secret (often JSON) and use it to connect to the database.
        # print(f"Secret content: {db_secret}") # Be cautious about printing sensitive information
    except Exception as e:
        print(f"Failed to fetch database secret: {e}")
