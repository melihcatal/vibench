import boto3

def rotate_secret_version(secret_name, version_stage):
    client = boto3.client('secretsmanager')
    response = client.describe_secret(SecretId=secret_name)
    for version in response['VersionIdsToStages']:
        if version_stage in response['VersionIdsToStages'][version]:
            return client.get_secret_value(SecretId=secret_name, VersionStage=version_stage)['SecretString']