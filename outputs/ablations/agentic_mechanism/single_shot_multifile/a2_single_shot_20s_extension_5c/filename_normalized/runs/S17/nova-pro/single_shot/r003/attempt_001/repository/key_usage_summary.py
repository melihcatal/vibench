from security_client import get_kms_client

def key_usage_summary():
    client = get_kms_client()
    response = client.describe_key(KeyId='alias/myKey')
    return response['KeyMetadata']