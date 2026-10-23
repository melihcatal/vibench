import boto3
import json


def parse_json_secret(secret_id):
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_id)
    secret_json = json.loads(response["SecretString"])
    return secret_json
