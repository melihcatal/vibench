from security_client import get_aws_secretsmanager_client


def fetch_api_key(secret_name):
    client = get_aws_secretsmanager_client()
    response = client.get_secret_value(SecretId=secret_name)
    return response["SecretString"]
