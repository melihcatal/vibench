import boto3

def fetch_api_key(secret_name):
    client = boto3.client('secretsmanager')
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    return get_secret_value_response['SecretString']