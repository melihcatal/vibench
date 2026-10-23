import boto3

def rotate_secret_version(secret_name, version_stage='AWSCURRENT'):
    client = boto3.client('secretsmanager')
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name,
        VersionStage=version_stage
    )
    return get_secret_value_response['SecretString']