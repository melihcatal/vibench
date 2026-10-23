import boto3


def fetch_db_secret():
    client = boto3.client("secretsmanager")
    secret_name = "DB_CONNECTION"
    response = client.get_secret_value(SecretId=secret_name)
    return response["SecretString"]
