import boto3


def key_usage_summary(key_id):
    client = boto3.client("kms")
    response = client.describe_key(KeyId=key_id)
    return response["KeyMetadata"]
