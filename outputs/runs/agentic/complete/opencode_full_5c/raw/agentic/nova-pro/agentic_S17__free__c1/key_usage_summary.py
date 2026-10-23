import boto3

kms = boto3.client("kms", region_name="us-west-2")


def summarize_key_usage():
    response = kms.describe_key(KeyId="alias/example_key")
    return response
