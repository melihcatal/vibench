import boto3


def get_secrets_client(region_name):
    return boto3.client("secretsmanager", region_name=region_name)


def normalize_secret_response(response):
    return response["SecretString"]
