import boto3
import json


def parse_json_secret(secret_name):
    client = boto3.client("secretsmanager", region_name="us-west-2")
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])
