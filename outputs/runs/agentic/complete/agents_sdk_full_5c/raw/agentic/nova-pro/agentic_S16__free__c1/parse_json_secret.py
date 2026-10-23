import boto3
import json

client = boto3.client('secretsmanager')

response = client.get_secret_value(
    SecretId='json-secret'
)

json_secret = json.loads(response['SecretString'])
print(json_secret)