import boto3
import json

client = boto3.client('secretsmanager')

def parse_json_secret(secret_name):
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])