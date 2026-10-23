import boto3


def fetch_db_secret():
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId="db-secret")
    return response["SecretString"]
