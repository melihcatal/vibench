import boto3

def rotate_secret_version(secret_id, version_stage='AWSCURRENT'):
    client = boto3.client('secretsmanager')
    describe_secret_response = client.describe_secret(SecretId=secret_id)
    versions = describe_secret_response['VersionIdsToStages']
    for version_id, stages in versions.items():
        if version_stage in stages:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_id,
                VersionId=version_id
            )
            return get_secret_value_response['SecretString']