from boto3 import client


def key_usage_summary():
    kms_client = client("kms")
    response = kms_client.list_keys()
    return response["Keys"]
