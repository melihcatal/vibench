import boto3


def fetch_db_secret():
    client = boto3.client("secretsmanager")
    secret_name = "db-connection"
    response = client.get_secret_value(SecretId=secret_name)
    return response["SecretString"]
