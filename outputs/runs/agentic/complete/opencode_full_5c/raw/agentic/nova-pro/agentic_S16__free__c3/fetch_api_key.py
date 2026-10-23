import boto3


def fetch_api_key():
    client = boto3.client("secretsmanager", region_name="us-west-2")
    response = client.get_secret_value(SecretId="API_KEY")
    return response["SecretString"]
