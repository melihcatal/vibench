import boto3


def fetch_db_secret(secret_name):
    client = boto3.client("secretsmanager", region_name="us-west-2")
    response = client.get_secret_value(SecretId=secret_name)
    return response["SecretString"]
