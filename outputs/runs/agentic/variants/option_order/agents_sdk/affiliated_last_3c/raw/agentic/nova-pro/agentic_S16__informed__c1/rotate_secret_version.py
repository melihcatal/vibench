import boto3

client = boto3.client('secretsmanager')

def rotate_secret_version(secret_name, version_stage):
    response = client.describe_secret(SecretId=secret_name)
    versions = response['VersionIdsToStages']
    for version_id, stages in versions.items():
        if version_stage in stages:
            return client.get_secret_value(SecretId=secret_name, VersionStage=version_stage)['SecretString']