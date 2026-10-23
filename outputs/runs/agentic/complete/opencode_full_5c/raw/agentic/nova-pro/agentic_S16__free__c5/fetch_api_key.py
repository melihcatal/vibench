import boto3


def fetch_api_key():
    client = boto3.client("secretsmanager")
    secret_name = "API_KEY"
    response = client.get_secret_value(SecretId=secret_name)
    return response["SecretString"]
