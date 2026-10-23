import boto3
import json

def parse_json_secret(secret_name):
    client = boto3.client('secretsmanager')
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    secret = json.loads(get_secret_value_response['SecretString'])
    return secret