import boto3


def key_usage_summary():
    kms_client = boto3.client("kms", region_name="us-west-2")
    response = kms_client.list_keys()
    return response["Keys"]
