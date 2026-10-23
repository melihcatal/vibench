import boto3


def get_security_client(region):
    return boto3.client("kms", region_name=region)


def get_config(region, key_id):
    return {
        "region": region,
        "key_id": key_id
    }