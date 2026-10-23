import boto3

def get_secret(secret_name, version_stage=None):
    client = boto3.client('secretsmanager')
    if version_stage:
        response = client.get_secret_value(
            SecretId=secret_name,
            VersionStage=version_stage
        )
    else:
        response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

# Example usage
secret_name = 'my-secret'
version_stage = 'AWSCURRENT'
secret_value = get_secret(secret_name, version_stage)
print(secret_value)