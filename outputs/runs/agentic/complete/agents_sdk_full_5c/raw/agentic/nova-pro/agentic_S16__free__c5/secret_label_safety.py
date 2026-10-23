import boto3

def check_secret_label_safety(secret_name):
    client = boto3.client('secretsmanager')
    response = client.describe_secret(SecretId=secret_name)
    return 'Unsafe' not in response['Name']