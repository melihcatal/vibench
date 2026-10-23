import boto3


def fetch_db_secret():
    client = boto3.client("secretsmanager", region_name="us-west-2")
    response = client.get_secret_value(SecretId="DB_CONNECTION_SECRET")
    return response["SecretString"]
