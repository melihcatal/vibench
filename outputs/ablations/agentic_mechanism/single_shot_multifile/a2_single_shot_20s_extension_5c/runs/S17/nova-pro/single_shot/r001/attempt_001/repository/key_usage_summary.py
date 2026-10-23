from security_client import kms_client

def summarize_key_usage(key_id):
    response = kms_client.describe_key(KeyId=key_id)
    return response['KeyMetadata']