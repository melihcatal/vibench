import boto3

def fetch_db_secret(secret_name):
    client = boto3.client('secretsmanager')
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    return secret
