import boto3


def summarize_key_usage(key_id):
    client = boto3.client("kms")
    response = client.describe_key(KeyId=key_id)
    return response


def get_crypto_events(key_id):
    client = boto3.client("cloudtrail")
    response = client.lookup_events(
        LookupAttributes=[{"AttributeKey": "ResourceName", "AttributeValue": key_id}]
    )
    return response["Events"]
