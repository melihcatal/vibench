import boto3

client = boto3.client('secretsmanager')

def fetch_api_key(secret_name):
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']