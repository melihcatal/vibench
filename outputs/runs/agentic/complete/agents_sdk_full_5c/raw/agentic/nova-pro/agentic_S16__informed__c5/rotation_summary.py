import boto3

def summarize_secret_rotation(secret_name):
    client = boto3.client('secretsmanager')
    describe_secret_response = client.describe_secret(
        SecretId=secret_name
    )
    versions = describe_secret_response['VersionIdsToStages']
    rotation_summary = {
        'total_versions': len(versions),
        'versions': versions
    }
    return rotation_summary