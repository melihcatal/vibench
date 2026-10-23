import boto3

kms = boto3.client("kms", region_name="us-west-2")


def key_usage_summary():
    response = kms.describe_key(KeyId="alias/myKey")
    return response
