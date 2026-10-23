import boto3
import json

def parse_json_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    secret_string = response['SecretString']
    return json.loads(secret_string)