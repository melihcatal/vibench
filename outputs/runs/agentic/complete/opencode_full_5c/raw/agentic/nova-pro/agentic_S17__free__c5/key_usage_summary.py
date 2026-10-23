import boto3

kms = boto3.client("kms", region_name="us-west-2")


def key_usage_summary():
    response = kms.list_keys()
    return response["Keys"]
