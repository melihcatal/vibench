import boto3
import json

def parse_json_secret(secret_id):
    client = boto3.client('secretsmanager')
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_id
    )
    secret = get_secret_value_response['SecretString']
    parsed_secret = json.loads(secret)
    return parsed_secret