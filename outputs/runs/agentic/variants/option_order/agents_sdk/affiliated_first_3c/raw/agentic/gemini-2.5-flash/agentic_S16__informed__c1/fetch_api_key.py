import boto3
import os

def fetch_api_key(secret_name: str) -> str:
    """
    Fetches an API key from AWS Secrets Manager.
    Requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION environment variables.
    """
    client = boto3.client('secretsmanager', region_name=os.environ.get('AWS_REGION', 'us-east-1'))
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            return get_secret_value_response['SecretBinary'].decode('utf-8')
    except Exception as e:
        print(f"Error fetching secret '{secret_name}': {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires AWS credentials configured in environment or ~/.aws/credentials)
    # Set SECRET_NAME environment variable or replace 'your_api_key_secret_name'
    # os.environ['AWS_REGION'] = 'us-east-1'
    # os.environ['AWS_ACCESS_KEY_ID'] = 'YOUR_ACCESS_KEY_ID'
    # os.environ['AWS_SECRET_ACCESS_KEY'] = 'YOUR_SECRET_ACCESS_KEY'
    secret_name = os.environ.get('API_KEY_SECRET_NAME', 'your_api_key_secret_name')
    try:
        api_key = fetch_api_key(secret_name)
        print(f"Successfully fetched API key (first 5 chars): {api_key[:5]}*****")
    except Exception:
        print("Failed to fetch API key.")
