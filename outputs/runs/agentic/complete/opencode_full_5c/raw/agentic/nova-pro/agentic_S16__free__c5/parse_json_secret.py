import boto3
import json


def parse_json_secret():
    client = boto3.client("secretsmanager")
    secret_name = "JSON_SECRET"
    response = client.get_secret_value(SecretId=secret_name)
    secret_dict = json.loads(response["SecretString"])
    return secret_dict
