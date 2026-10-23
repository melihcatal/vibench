import boto3

# Configuration
AWS_REGION = 'us-west-2'
SECRET_NAME = 'my_secret'

# Initialize the Secrets Manager client
secrets_manager_client = boto3.client('secretsmanager', region_name=AWS_REGION)

def get_secret():
    try:
        get_secret_value_response = secrets_manager_client.get_secret_value(
            SecretId=SECRET_NAME
        )
        secret = get_secret_value_response['SecretString']
        return secret
    except Exception as e:
        print(f'Error retrieving secret: {e}')
        return None
