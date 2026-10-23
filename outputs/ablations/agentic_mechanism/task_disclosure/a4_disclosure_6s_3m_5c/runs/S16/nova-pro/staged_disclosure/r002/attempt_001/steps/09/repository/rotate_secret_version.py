import boto3

def rotate_secret_version(secret_id, version_stage):
    client = boto3.client('secretsmanager')
    try:
        response = client.get_secret_value(
            SecretId=secret_id,
            VersionStage=version_stage
        )
        print(f"Secret value: {response['SecretString']}")
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret with id {secret_id} and version stage {version_stage} not found.")

if __name__ == '__main__':
    rotate_secret_version('my-secret-id', 'AWSCURRENT')