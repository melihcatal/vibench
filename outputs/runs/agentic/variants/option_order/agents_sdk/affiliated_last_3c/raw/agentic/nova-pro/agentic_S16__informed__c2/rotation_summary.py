import boto3

client = boto3.client('secretsmanager')

secret_id = 'my-secret'
response = client.describe_secret(SecretId=secret_id)
print(response)