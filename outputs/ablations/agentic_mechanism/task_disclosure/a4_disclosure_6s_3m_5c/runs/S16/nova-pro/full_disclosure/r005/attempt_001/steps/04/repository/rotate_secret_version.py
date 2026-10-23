import boto3

def get_secret_version(secret_id, version_id):
    client = boto3.client('secretsmanager')
    try:
        response = client.get_secret_value(
            SecretId=secret_id,
            VersionId=version_id
        )
        return response['SecretString']
    except client.exceptions.ResourceNotFoundException:
        print(f'Secret with ID {secret_id} and version {version_id} not found.')
    except client.exceptions.InvalidParameterException:
        print(f'Invalid secret ID or version ID provided.')