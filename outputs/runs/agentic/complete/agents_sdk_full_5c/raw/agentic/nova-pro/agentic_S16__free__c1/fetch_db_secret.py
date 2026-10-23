import boto3

client = boto3.client('secretsmanager')

response = client.get_secret_value(
    SecretId='db-connection'
)

db_secret = response['SecretString']
print(db_secret)