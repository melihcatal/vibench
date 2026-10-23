import boto3

def summarize_rotation_status(secret_id):
    client = boto3.client('secretsmanager')
    describe_secret_response = client.describe_secret(SecretId=secret_id)
    versions = describe_secret_response['VersionIdsToStages']
    return versions