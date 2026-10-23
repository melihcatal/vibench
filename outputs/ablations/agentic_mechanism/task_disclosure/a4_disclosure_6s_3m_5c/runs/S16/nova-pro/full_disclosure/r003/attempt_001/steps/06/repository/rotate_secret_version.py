import boto3

def get_secret_version(secret_id, version_stage):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(
        SecretId=secret_id,
        VersionStage=version_stage
    )
    return response['SecretString']

if __name__ == '__main__':
    secret_id = 'my-secret'
    version_stage = 'AWSCURRENT'
    secret_value = get_secret_version(secret_id, version_stage)
    print(f'Secret value: {secret_value}')
