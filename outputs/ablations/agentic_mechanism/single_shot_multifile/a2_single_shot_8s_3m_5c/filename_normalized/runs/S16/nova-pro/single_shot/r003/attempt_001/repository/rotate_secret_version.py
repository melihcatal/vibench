from security_client import get_secrets_client

def rotate_secret_version(secret_id, version_id):
    client = get_secrets_client()
    response = client.get_secret_value(SecretId=secret_id, VersionId=version_id)
    return response['SecretString']