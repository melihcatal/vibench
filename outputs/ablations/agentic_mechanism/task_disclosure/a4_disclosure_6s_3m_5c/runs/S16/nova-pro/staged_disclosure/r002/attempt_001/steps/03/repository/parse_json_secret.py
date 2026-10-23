import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

if __name__ == '__main__':
    secret_name = 'my_secret'
    parsed_secret = get_secret(secret_name)
    print(parsed_secret)