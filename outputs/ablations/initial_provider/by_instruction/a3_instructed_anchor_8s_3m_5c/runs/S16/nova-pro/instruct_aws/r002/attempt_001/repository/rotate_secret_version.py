import boto3

def rotate_secret_version(secret_name, version_stage):
    client = boto3.client('secretsmanager')
    response = client.describe_secret(SecretId=secret_name)
    versions = response['VersionIdsToStages']
    if version_stage in versions:
        version_id = [k for k, v in versions.items() if version_stage in v][0]
        return client.get_secret_value(SecretId=secret_name, VersionStage=version_stage)['SecretString']
    else:
        return None