import boto3


def fetch_api_key(secret_id):
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_id)
    return response["SecretString"]
