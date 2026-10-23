import boto3


def key_usage_summary():
    client = boto3.client("kms", region_name="us-west-2")
    response = client.list_keys()
    return response["Keys"]
