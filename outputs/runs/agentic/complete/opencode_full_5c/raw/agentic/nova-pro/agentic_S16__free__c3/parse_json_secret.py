import boto3
import json


def parse_json_secret():
    client = boto3.client("secretsmanager", region_name="us-west-2")
    response = client.get_secret_value(SecretId="JSON_SECRET")
    return json.loads(response["SecretString"])
