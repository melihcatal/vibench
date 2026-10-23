import boto3

client = boto3.client('secretsmanager')

response = client.get_secret_value(
    SecretId='api-key',
    VersionStage='AWSCURRENT'
)

api_key = response['SecretString']
print(api_key)