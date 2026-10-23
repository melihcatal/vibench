import boto3


def fetch_api_key():
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId="api-key")
    return response["SecretString"]
