import boto3

def rotate_secret_version(secret_name, version_stage='AWSCURRENT'):
    client = boto3.client('secretsmanager')
    response = client.describe_secret(SecretId=secret_name)
    for version in response['VersionIdsToStages']:
        if version_stage in response['VersionIdsToStages'][version]:
            get_response = client.get_secret_value(SecretId=secret_name, VersionId=version)
            return get_response['SecretString']