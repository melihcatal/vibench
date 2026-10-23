import boto3
import json


def parse_json_secret():
    client = boto3.client("secretsmanager")
    secret_name = "json-secret"
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])
