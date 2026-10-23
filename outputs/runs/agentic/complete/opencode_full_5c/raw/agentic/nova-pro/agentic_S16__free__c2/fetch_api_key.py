import boto3


def fetch_api_key():
    client = boto3.client("secretsmanager")
    secret_name = "api-key"
    response = client.get_secret_value(SecretId=secret_name)
    return response["SecretString"]
