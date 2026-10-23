import boto3


def get_secrets_client(region_name="us-west-2"):
    return boto3.client("secretsmanager", region_name=region_name)


def get_secret(secret_name):
    client = get_secrets_client()
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    return get_secret_value_response["SecretString"]
