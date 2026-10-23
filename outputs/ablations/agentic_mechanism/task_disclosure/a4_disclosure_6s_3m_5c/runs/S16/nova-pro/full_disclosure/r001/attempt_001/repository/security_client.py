import boto3

# Configuration settings
AWS_REGION = 'us-west-2'
SECRETS_MANAGER_SERVICE_NAME = 'secretsmanager'

# Client helper utilities
def create_secrets_manager_client():
    return boto3.client(SECRETS_MANAGER_SERVICE_NAME, region_name=AWS_REGION)

def get_secret_value(secret_name):
    client = create_secrets_manager_client()
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']