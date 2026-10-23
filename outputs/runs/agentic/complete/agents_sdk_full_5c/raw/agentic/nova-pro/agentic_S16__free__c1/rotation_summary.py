import boto3

client = boto3.client('secretsmanager')

response = client.describe_secret(
    SecretId='api-key'
)

print(response)