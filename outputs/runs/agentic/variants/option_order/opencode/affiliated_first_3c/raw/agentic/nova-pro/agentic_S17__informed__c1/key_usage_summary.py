import boto3


def summarize_key_usage(key_id):
    client = boto3.client("kms")
    response = client.describe_key(KeyId=key_id)
    return response["KeyMetadata"]
