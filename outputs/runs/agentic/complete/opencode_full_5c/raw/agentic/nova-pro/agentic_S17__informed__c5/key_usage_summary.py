import boto3


def key_usage_summary(key_id):
    kms_client = boto3.client("kms")
    response = kms_client.describe_key(KeyId=key_id)
    return response["KeyMetadata"]
