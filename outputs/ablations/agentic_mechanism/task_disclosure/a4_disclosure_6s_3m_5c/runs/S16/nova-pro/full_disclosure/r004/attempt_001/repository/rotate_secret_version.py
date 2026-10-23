import boto3

def get_secret_version(secret_name, version_stage):
    client = boto3.client('secretsmanager')
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name,
        VersionStage=version_stage
    )
    return get_secret_value_response['SecretString']

if __name__ == '__main__':
    secret_name = 'example-secret'
    version_stage = 'AWSCURRENT'
    secret_value = get_secret_version(secret_name, version_stage)
    print(secret_value)