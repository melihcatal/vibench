import boto3
from botocore.exceptions import ClientError


def key_usage_summary():
    client = boto3.client("kms")
    try:
        response = client.list_keys()
        return response["Keys"]
    except ClientError as e:
        print(e)
        return None
