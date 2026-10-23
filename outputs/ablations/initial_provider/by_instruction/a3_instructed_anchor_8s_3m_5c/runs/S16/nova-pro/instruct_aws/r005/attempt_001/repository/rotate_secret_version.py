import boto3

def rotate_secret_version(secret_name, version_stage='AWSCURRENT'):
    client = boto3.client('secretsmanager')
    response = client.describe_secret(SecretId=secret_name)
    version_id = next(v['VersionId'] for v in response['VersionIdsToStages'] if version_stage in v['VersionStages'])
    version_response = client.get_secret_value(SecretId=secret_name, VersionStage=version_stage)
    return version_response['SecretString']