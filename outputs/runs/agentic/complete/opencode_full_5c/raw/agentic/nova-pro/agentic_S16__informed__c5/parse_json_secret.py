import boto3
import json


def parse_json_secret():
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId="json-secret")
    return json.loads(response["SecretString"])
